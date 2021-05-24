# requires 'npm i -g autodidact'
autodidact openshift.adoc 

asciidoctor -a data-uri -a image-prefix=./images/ openshift.adoc.didact.adoc  -o openshift.didact.md
rm openshift.adoc.didact.adoc

if [[ "$OSTYPE" == "darwin"* ]]; then

  # macOS OSX
open openshift.didact.md

elif

xdg-open openshift.didact.md

fi

