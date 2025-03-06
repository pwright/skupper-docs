# Linking sites on Kubernetes

Linking sites allows you expose services from one site and consume those services on another site.
You can link sites using the following methods:

* Using the CLI to create tokens
* Using YAML to create tokens
* Using direct linking

## Linking sites on Kubernetes using the Skupper CLI

Using the skupper command-line interface (CLI) allows you to create links between sites.

.Prerequisites

* Two sites
* At least one site with `enable-link-access` enabled.

To link sites, you create a token on one site and redeem that token on the other site to create the link.

.Procedure

1. On the site where you want to issue the token, make sure link access is enabled:
   ```bash
   skupper site update --enable-link-access
   ```
2. Create a token:
   ```bash
   skupper token issue <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

   This file contains a key and the location of the site that created it.
   
   **📌 NOTE**
   Access to this file provides access to the application network. 
   Protect it appropriately.
   A token can be restricted by:

   * expiration-window  - prevents token reuse after a specified period. The default is 15 minutes.
   * redemptions-allowed - prevents creating more links from a single token than planned. The default is 1.
   
   All inter-site traffic is protected by mutual TLS using a private, dedicated certificate authority (CA).
   A token is not a certificate, but is securely exchanged for a certificate during the linking process.
   By implementing appropriate restrictions (for example, creating a single-use claim token), you can avoid the accidental exposure of certificates.


3. Redeem the token on a different site to create a link:
   ```bash
   skupper token redeem <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   You might need to issue the command multiple times before the link is ready:
   ```
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Pending 1       Not Operational
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Ready   1       OK
   ```
   You can now expose services on the application network.

There are many options to consider when linking sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.


## Linking sites on Kubernetes using YAML

You can use YAML to link sites.

.Prerequisites

* Two sites
* At least one site with `linkAccess` set.

.Procedure

1. On the site where you want to issue the token, make sure link access is enabled:
   ```bash
   kubectl get site -o yaml|grep linkAccess
   ```
   For example
   ```
    $ kubectl get site -o yaml|grep linkAccess
        linkAccess: default
   ```
2. Create an AccessToken YAML file:
   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: AccessToken
   metadata:
     name: my-token
   spec:   
   ```
   This YAML creates an AccessToken named `my-token` in the context of the current namespace.

3. Retrieve the AccessGrant name:
   ```bash
   kubectl get AccessGrant
   ```
   For example:
   ```
   $ kubectl get accessgrant
   NAME                                        REDEMPTIONS ALLOWED   REDEMPTIONS MADE   EXPIRATION             STATUS   MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a   1                     1                  2025-02-24T10:49:59Z   Ready    OK
   ```

4. Create a token file from the AccessGrant:
   ```bash
    kubectl get accessgrant/west-403a24f6-6872-46f9-89d3-baf1162cabaf -o template --template '
    apiVersion: skupper.io/v2alpha1
    kind: AccessToken
    metadata:
      name: my-token
    spec:
      code: "{{ .status.code }}"
      ca: {{ printf "%q" .status.ca }}
      url: "{{ .status.url }}"
    ' > <filename>
    ```

   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

   This file contains a key and the location of the site that created it.
   
3. Redeem the token on a different site to create a link:
   ```bash
   kubectl apply -f <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

4. Check the status of the link:
   ```bash
   kubectl get link
   ```
   You might need to issue the command multiple times before the link is ready:
   ```
   $ skupper get link
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Pending 1       Not Operational
   $ skupper get link
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Ready   1       OK
   ```
   You can now expose services on the application network.


There are many options to consider when linking sites using YAML, see [YAML Reference][yaml-ref], including *frequently used* options.

[cli-ref]: https://skupperproject.github.io/refdog/commands/index.html
[yaml-ref]: https://skupperproject.github.io/refdog/resources/index.html

## Linking sites directly

You can also create links between sites directly as an alternative to creating tokens.

.Prerequisites

* Two sites
* At least one site with `enable-link-access` enabled.

To link sites, you create a token on one site and redeem that token on the other site to create the link.

.Procedure

1. On the site where you want to issue the token, make sure link access is enabled:
   ```bash
   skupper site update --enable-link-access
   ```
2. Create a link resource:
   ```bash
   skupper link generate > <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

   This file contains TLS certs and the location of the site that created it.
   
   **📌 NOTE**
   Access to this file provides access to the application network. 
   Protect it appropriately.

   All inter-site traffic is protected by mutual TLS using a private, dedicated certificate authority (CA).
   A token is not a certificate, but is securely exchanged for a certificate during the linking process.
   By implementing appropriate restrictions (for example, creating a single-use claim token), you can avoid the accidental exposure of certificates.


3. Use the link resource on a different site to create a link:
   ```bash
   kubectl apply -f <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   You might need to issue the command multiple times before the link is ready:
   ```
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Pending 1       Not Operational
   $ skupper link status
   NAME                                            STATUS  COST    MESSAGE
   west-12f75bc8-5dda-4256-88f8-9df48150281a       Ready   1       OK
   ```
   You can now expose services on the application network.

There are many options to consider when linking sites using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

