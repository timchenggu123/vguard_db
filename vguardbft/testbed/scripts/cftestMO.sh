#!/bin/bash

timehost=1
timeofollower=2
timelfollower=$4

# i=1
# while IFS= read -r line; do 
#     # ssh $line "echo \"cd ./go/src/vguard/scripts; ./cftestHost.sh $1 $i $3\" | at $timehost" &
#     ssh $line "cd ./go/src/vguard/scripts; ./cftestHost.sh $1 $i $3" &
# 
#     ((i++))
#     if [ $i -gt $2 ]; then
#         break
#     fi
# done < serverlist
# sleep 0.5

i=1
while IFS= read -r line; do 
    # ssh $line "echo \"cd ./go/src/vguard/scripts; ./cftestOtherFollowers.sh $1 $i $2\" | at $timeofollower" &
    ssh $line "cd ./go/src/vguard/scripts; ./cftestOtherFollowers.sh $1 $i $2" &

    ((i++))
    if [ $i -gt $1 ]; then
        break
    fi
done < serverlist
sleep 0.5

# i=$1
# let "lfend=$1-$2+1"
# while IFS= read -r line; do 
#     # ssh $line "echo \"cd ./go/src/vguard/scripts; ./cftestLastFollowers.sh $1 $i\" | at $timelfollower" &
#     ssh $line "cd ./go/src/vguard/scripts; ./cftestLastFollowers.sh $1 $i" &
# 
#     sleep 0.3
#     ((i--))
#     if [ $i -lt $lfend ]; then
#         break
#     fi
# done < serverlist
