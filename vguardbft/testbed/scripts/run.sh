#!/bin/bash
# test in localhost
#./vguard -id=$1 -log=4 -r=$2 -s=true -cs=10

# run in cluster
./vguard -id=$1 -log=3 -r=$2 -s=false -es=1 -cfp=./config/cluster_$3.conf -n=$3
