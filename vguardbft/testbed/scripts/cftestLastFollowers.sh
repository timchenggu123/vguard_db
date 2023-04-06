#!/bin/bash

# let "cfNum=$1-$2+1"
# let "halfTotal=$1/2"
# id=$2
# if [ $id -gt $halfTotal ]; then
# 	((id--))
# fi

# let "sleeptime=$2/2+10"
cd ..
echo "start the last follower: id $3, leader: $4"
# echo "sleeping $sleeptime seconds"
# sleep $sleeptime
# ./vguard -r=1 -log=3 -s=false -n=$1 -id=$3 -cfp=./config/cluster_$1_cf_$4.conf 
echo "sleep $2; cd ~/go/src/vguard; ./vguard -r=1 -log=3 -s=false -n=$1 -id=$3 -cfp=./config/cluster_$1_cf_$4.conf &" | at ${5:-now}
