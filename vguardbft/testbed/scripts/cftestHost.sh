#!/bin/bash

cd ..
echo "starting host: id $2"
./vguard -id=0 -log=4 -r=0 -s=true -b=1 -es=1 -ml=5000 -m=$3 -n=$1 -cfp=./config/cluster_$1_cf_$2.conf &
