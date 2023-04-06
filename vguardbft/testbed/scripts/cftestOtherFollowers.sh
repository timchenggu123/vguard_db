#!/bin/bash

i=1
let "idp=$2-1"
let "lastid=$1-$2+1"
cd ..

while [[ $i -lt $2 && $i -le $3 ]]; do
    if [ $i -eq $lastid ]; then
        ((i++))
        continue
    fi
    echo "starting follower $2: id $idp, leader $i"
    ./vguard -r=1 -log=3 -s=false -n=$1 -id=$idp -cfp=./config/cluster_$1_cf_$i.conf &
    ((i++))
    sleep 1
done
((i++))
while [ $i -le $3 ]; do
    if [ $i -eq $lastid ]; then
	    ((i++))
        continue
    fi
    echo "starting follower $2: id $2, leader $i"
    ./vguard -r=1 -log=3 -s=false -n=$1 -id=$2 -cfp=./config/cluster_$1_cf_$i.conf &
    ((i++))
    sleep 1
done
