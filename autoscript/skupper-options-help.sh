grep -o '^[^,]\+' skupper-options-help.csv | while read -r line ; do
    linename=`echo $line | sed 's/[[:space:]]//g'`
    echo "[id=$linename]"
    echo "== The skupper '$line' option"
    echo "// tag::$linename[]"
    echo "----"
    skupper $line -h
    echo "----"
    echo "// end::$linename[]"

done