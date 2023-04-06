#!/bin/bash

i=1

es=100000
ml=10000000
if [ $2 -eq 1 ]; then
    es=1
    ml=50000
fi

# read -p "---------- executing commands remotely? --------------"
# while IFS= read -r line; do
#     echo "starting host on server $i -> id: $line"

#     # set up hosts
#     ssh $line "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_$i.conf" &
#     echo "host $i -> $line is done"

#     ((i++))
#     if [[ $i -gt $1 ]]; then
# 	    break
# 	fi
# done < serverlist

if [ $1 -ge 4 ]; then 
    echo "starting hosts"
    ssh vp-8 "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_1.conf" &
    ssh vp-7 "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_2.conf" &
    ssh vp-6 "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_3.conf" &
    ssh vp-5 "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_4.conf" &

    echo "hosts done"
    sleep 1
    echo "starting followers in the first round"

    ssh vp-8 "cd ./go/src/vguard; ./vguard -id=1 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_2.conf" &
    ssh vp-8 "cd ./go/src/vguard; ./vguard -id=1 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_3.conf" &

    ssh vp-7 "cd ./go/src/vguard; ./vguard -id=1 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &
    ssh vp-7 "cd ./go/src/vguard; ./vguard -id=2 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_4.conf" &

    ssh vp-6 "cd ./go/src/vguard; ./vguard -id=2 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &
    ssh vp-6 "cd ./go/src/vguard; ./vguard -id=3 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_4.conf" &

    ssh vp-5 "cd ./go/src/vguard; ./vguard -id=3 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_2.conf" &
    ssh vp-5 "cd ./go/src/vguard; ./vguard -id=3 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_3.conf" &
    
    echo "n-1 followers done"
    sleep 0.5
    echo "starting the last followers"

    ssh vp-5 "cd ./go/src/vguard; ./vguard -id=3 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &

    ssh vp-6 "cd ./go/src/vguard; ./vguard -id=2 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_2.conf" &

    ssh vp-7 "cd ./go/src/vguard; ./vguard -id=2 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_3.conf" &
    
    ssh vp-8 "cd ./go/src/vguard; ./vguard -id=1 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_4.conf" &

elif [ $1 -eq 3 ]; then 
    echo "starting hosts"
    ssh vp-8 "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_1.conf" &
    ssh vp-7 "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_2.conf" &
    ssh vp-6 "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_3.conf" &

    echo "hosts done"
    sleep 1
    echo "starting followers in the first round"

    ssh vp-8 "cd ./go/src/vguard; ./vguard -id=1 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_2.conf" &
    ssh vp-8 "cd ./go/src/vguard; ./vguard -id=1 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_3.conf" &

    ssh vp-7 "cd ./go/src/vguard; ./vguard -id=1 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &

    ssh vp-6 "cd ./go/src/vguard; ./vguard -id=2 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &

    ssh vp-5 "cd ./go/src/vguard; ./vguard -id=3 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_2.conf" &
    ssh vp-5 "cd ./go/src/vguard; ./vguard -id=3 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_3.conf" &

    echo "n-1 followers done"
    sleep 0.5
    echo "starting the last followers"

    ssh vp-5 "cd ./go/src/vguard; ./vguard -id=3 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &

    ssh vp-6 "cd ./go/src/vguard; ./vguard -id=2 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_2.conf" &

    ssh vp-7 "cd ./go/src/vguard; ./vguard -id=2 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_3.conf" &

elif [ $1 -eq 2 ]; then 
    echo "starting hosts"
    ssh vp-8 "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_1.conf" &
    ssh vp-7 "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_2.conf" &

    echo "hosts done"
    sleep 1
    echo "starting followers in the first round"

    ssh vp-8 "cd ./go/src/vguard; ./vguard -id=1 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_2.conf" &

    ssh vp-7 "cd ./go/src/vguard; ./vguard -id=1 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &

    ssh vp-6 "cd ./go/src/vguard; ./vguard -id=2 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &

    ssh vp-5 "cd ./go/src/vguard; ./vguard -id=3 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_2.conf" &

    echo "n-1 followers done"
    sleep 0.5
    echo "starting the last followers"

    ssh vp-5 "cd ./go/src/vguard; ./vguard -id=3 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &

    ssh vp-6 "cd ./go/src/vguard; ./vguard -id=2 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_2.conf" &

elif [ $1 -eq 1 ]; then 
    echo "starting hosts"
    ssh vp-8 "cd ./go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -n=4 -b=$2 -es=$es -ml=$ml -m=$3 -cfp=./config/cluster_4_cf_1.conf" &

    echo "hosts done"
    sleep 1
    echo "starting followers in the first round"

    ssh vp-7 "cd ./go/src/vguard; ./vguard -id=1 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &

    ssh vp-6 "cd ./go/src/vguard; ./vguard -id=2 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &

    echo "n-1 followers done"
    sleep 0.5
    echo "starting the last followers"

    ssh vp-5 "cd ./go/src/vguard; ./vguard -id=3 -log=3 -r=1 -s=false -n=4 -cfp=./config/cluster_4_cf_1.conf" &

fi
