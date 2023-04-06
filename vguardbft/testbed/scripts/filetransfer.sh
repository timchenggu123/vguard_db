#!/bin/bash

i=0
read -p "---------- transfer files? --------------"
while IFS= read -r line; do
    echo "transferring to replica $i -> id: $line"
    scp -r ${1:-../../vguard}  $line:/home/ubuntu/go/src/${2:-}
    ((i++))
done < serverlist
