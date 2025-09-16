# Custom TLS Certificates

By default, the Skupper controller generates internal certificate authorities (CAs) and self-signed certificates.
For example, it creates certificates to authenticate incoming Skupper links from external Skupper sites.
This ensures all communication between sites is encrypted.

The following certificates are created automatically:

- `skupper-site-ca`: Default issuer for a Skupper site
- `skupper-site-server`: Server certificate for the `skupper-router` service

The server certificate is issued for the public hostname or IP address associated with the `skupper-router` service. The value depends on the ingress method, such as an OpenShift route or a Kubernetes LoadBalancer service.

You can override this behavior by providing your own server certificate or CA.


## Providing a custom server certificate for Kubernetes sites

### Prerequisites

- A valid server certificate that matches the public hostname or IP address of the site.
- Access to the namespace where the Skupper site is deployed.

### Procedure

0. Change context to the namespace of the site you want other sites to link to. For example:
   ```
   
   ```

1. Create a Kubernetes secret named `skupper-site-server` in the site namespace:
	```
	apiVersion: v1
	kind: Secret
	metadata:
	  name: skupper-site-server
	data:
	  ca.crt: LS0tLS1C...redacted
	  tls.crt: LS0tLS1C...redacted
	  tls.key: LS0tLS1C...redacted
	```
    For example if you have the following files:
   
    - `tls.crt` — PEM server certificate (with the right SANs for how peers connect).
    - `tls.key` — PEM private key for `tls.crt`.
    - `ca.crt` — PEM CA (or chain) that issued `tls.crt`.

    You can create the secret using the following commands:

    ```
    # Set paths (adjust as needed)
    TLS_CRT=./server.crt.pem
    TLS_KEY=./server.key.pem
    CA_CRT=./ca.crt.pem

    NAME=skupper-site-server

    # Create YAML then apply (works for create/update)
    kubectl create secret generic "$NAME" \
      --from-file="tls.crt=$TLS_CRT" \
      --from-file="tls.key=$TLS_KEY" \
      --from-file="ca.crt=$CA_CRT" \
      --dry-run=client -o yaml | kubectl apply -f -
    ```

2. If a site does not already exist, create the site.
   If the site already exists, restart the router using:
   ```
   kubectl rollout restart deploy/skupper-router
   ``` 

3. Verify the hostname or IP address of the site:
	```
	kubectl get site -o json | jq -r .items[].status.endpoints[0].host
	```
	Example output:
	```
	skupper.public.host
	```
	This value must match the value in the `tls.crt` certificate.

4. Confirm that Skupper detects your certificate:
	```
	kubectl get certificate skupper-site-server -o json | jq -r .status.conditions[].message
	```
	Example output:
	```
	Secret exists but is not controlled by skupper
	```
	This output indicates that Skupper recognizes the custom secret but does not manage it.


## Generating a link for remote sites

After configuring your site with a custom certificate, generate a link to share with remote sites.

### Option 1: Use the Skupper CLI

- If you provided the `skupper-site-ca` issuer:
	```
	skupper link generate
	```
- If you already created a client certificate secret named `skupper-link`:
	```
	skupper link generate --tls-credentials skupper-link
	```
- If you manage the client certificate yourself:
	```
	skupper link generate --generate-credential=false --tls-credentials=skupper-link
	```
	To combine with your client secret file:
	```
	skupper link generate --generate-credential=false --tls-credentials=skupper-link; echo "---"; cat client-secret.yaml
	```

### Option 2: Use `kubectl`

1. Extract the endpoints and generate a link:
	```
	endpoints=$(kubectl get site -o json | jq -r '.items[].status.endpoints')
	cat << EOF | yq -y --argjson endpoints "${endpoints}" '.spec.endpoints = $endpoints' | tee skupper-link.yaml
	apiVersion: skupper.io/v2alpha1
	kind: Link
	metadata:
	  name: skupper-link
	spec:
	  cost: 1
	  tlsCredentials: skupper-link
	EOF
	```
2. Append the client secret:
	```
	echo "---" >> skupper-link.yaml
	cat client-secret.yaml >> skupper-link.yaml
	```

### Option 3: Manually create the link

1. Retrieve the list of endpoints:
	```
	kubectl get site -o yaml | yq -y .items[].status.endpoints
	```
	Example output:
	```
	- group: skupper-router
	  host: skupper.public.host
	  name: inter-router
	  port: '55671'
	- group: skupper-router
	  host: skupper.public.host
	  name: edge
	  port: '45671'
	```
2. Create a YAML file containing both the link and client secret:
	```
	---
	apiVersion: skupper.io/v2alpha1
	kind: Link
	metadata:
	  name: skupper-link
	spec:
	  cost: 1
	  tlsCredentials: skupper-link
	  endpoints:
	    - group: skupper-router
	      host: skupper.public.host  # Must match the custom certificate
	      name: inter-router
	      port: '55671'
	    - group: skupper-router
	      host: skupper.public.host
	      name: edge
	      port: '45671'
	---
	apiVersion: v1
	kind: Secret
	metadata:
	  name: skupper-link
	data:
	  ca.crt: LS0tLS1C...redacted
	  tls.crt: LS0tLS1C...redacted
	  tls.key: LS0tLS1C...redacted
	```

---
