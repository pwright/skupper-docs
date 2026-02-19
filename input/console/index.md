<a id="console"></a>
# Using the Network console

The Network console provides data and visualizations of the traffic flow between sites.

<a id="console-enabling"></a>
## Enabling the Network console

**Prerequisites**

* A Kubernetes site


**Procedure**

1. Determine which site in your network is best to enable the Network console using the following criteria:

   * Does the application network cross a firewall? For example, if you want the console to be available only inside the firewall, you need to locate the Network console on a site inside the firewall.
   * Is there a site that processes more traffic than other sites? For example, if you have a frontend component that calls a set of services from other sites, it might make sense to locate the Network console on that site to minimize data traffic.
   * Is there a site with more or cheaper resources that you want to use? For example, if you have two sites, A and B, and resources are more expensive on site A, you might want to locate the Network console on site B.

2. Change context to a site namespace.

3. Deploy the network observer helm chart:
   ```
   helm install skupper-network-observer oci://quay.io/skupper/helm/network-observer --version {{skupper_cli_version}}
   ```

   The output is similar to the following:
   ```
   Pulled: quay.io/skupper/helm/network-observer:2.1.1
   Digest: sha256:557c8a3f4b5d8bb6e779a81e6214fa87c2ad3ad0c957a5c08b8dd3cb20fc7cfe
   NAME: skupper-network-observer
   LAST DEPLOYED: Sun Mar  9 19:47:09 2025
   NAMESPACE: default
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   NOTES:
   You have installed the skupper network observer!
   
   Accessing the console:
   The network-observer application is exposed as a service inside of your
   cluster. To access the application externally you must either enable an
   ingress of some sort or use port forwarding to access the service
   temporarily.
   Expose the application at https://127.0.0.1:8443 with the command:
   kubectl --namespace default port-forward service/skupper-network-observer 8443:443

   Basic Authentication is enabled.

   Users are configured in the skupper-network-observer-auth secret.
   This secret has been prepopulated with a single user "skupper" and a randomly
   generated password stored in plaintext. It is recommended that these
   credentials be rotated and replaced with a secure password hash (bcrypt.)
 
   Retrieve the password with this command:
   kubectl --namespace default \
         get secret skupper-network-observer-auth \
         -o jsonpath='{.data.htpasswd}' | base64 -d | sed 's/\(.*\):{PLAIN}\(.*\)/\1 \2\n/'
   ```
4. Expose the `skupper-network-observer` service to make the Network console available, for example on OpenShift:

   ```
   oc create route passthrough skupper-console --service=skupper-network-observer --port=https
   ```

<a id="console-exploring"></a>
## Exploring the Network console

The Network console provides an overview of the following:

* Topology
* Services
* Sites
* Components
* Processes

For example, consider the following service:

<img src="../images/console.png" alt="adservice in london and berlin" style="width: 100%;">
<!--
![services](../images/console.png)
-->

For more information, see [Configuring the Network observer](#configuring-network-observer)

<a id="configuring-network-observer"></a>
# Configuring the Network observer

Currently the primary purpose of the Network Observer is to provide a console for monitoring your application network.
Typically, you only need to follow the procedure in [Using the Network console](#console).
This section describes advanced configuration.


1. Change context to a site namespace.

2. Apply a CR to create the Network Observer instance

   The following CR shows the supported parameters that you can use to configure the Network observer instance:
   
   ```
   apiVersion: observability.skupper.io/v2alpha1
   kind: NetworkObserver
   metadata:
     name: networkobserver-sample
     namespace: west
   spec:
     # Resource requests and limits
     resources:
       requests:
         cpu: "250m"
         memory: "4Gi"
       limits:
         cpu: "1"
         memory: "8Gi"
   
     # Authentication strategies
     auth:
       # strategy is one of none, basic, or openshift
       strategy: "openshift"
       openshift:
         # createCookieSecret -
         # for the openshift oauth2 proxy.
         createCookieSecret: true
         # cookieSecretName name of the session cookie secret.
         cookieSecretName: ""
         # Service account for openshift auth
         serviceAccount:
           create: true
           nameOverride: ""
   ```

3. Verify the configuration, enter:

   ```
   oc describe networkobserver networkobserver-sample -n west
   ```
   
   Note that the parameters listed in output, not related to the CR above, are not configurable.
   
   
   If you require further configuration parameters, create a request in the [Skupper JIRA project](https://issues.redhat.com/projects/SKUPPER/).


**Troubleshooting**

If you are concerned about Network Observer resources, consider using standard techniques to monitor those resources, for example:

```
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: network-observer-memory-alert
  namespace: west
spec:
  groups:
  - name: network-observer.rules
    rules:
    - alert: NetworkObserverHighMemory
      expr: |
        (container_memory_working_set_bytes{namespace="west", container="network-observer"} 
        / 
        kube_pod_container_resource_limits{namespace="west", container="network-observer", resource="memory"}) > 0.9
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Network Observer pod in namespace {{ $labels.namespace }} is using > 90% of its memory limit."
        description: "Pod {{ $labels.pod }} is currently using {{ $value | humanizePercentage }} of its memory limit."
```

