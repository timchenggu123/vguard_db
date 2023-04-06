#!/bin/bash

i=1

read -p "---------- executing commands remotely? --------------"
while IFS= read -r line; do
    echo "add netlwork latency on server $i -> id: $line"
    ssh -tt $line "sudo tc qdisc add dev ens3 root netem delay $2ms $3ms distribution normal" &

    echo "server $i -> $line latency $2ms added"
    ((i++))
    if [[ $i -ge $1 ]]; then
	    break
	fi
done < serverlist
sudo tc qdisc add dev ens3 root netem delay $2ms $3ms distribution normal
echo "host latency $2ms added"
