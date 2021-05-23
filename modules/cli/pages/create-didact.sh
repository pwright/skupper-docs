# requires 'npm i -g autodidact'
autodidact openshift.adoc 

asciidoctor -a data-uri -a image-prefix=./images/ openshift.adoc.didact.adoc  -o openshift.didact.md
rm openshift.adoc.didact.adoc

open openshift.didact.md