#!/bin/bash

i=1

sudo tc qdisc del dev ens3 root
echo "host latency deleted"

read -p "---------- executing commands remotely? --------------"
while IFS= read -r line; do
    echo "delete netlwork latency on server $i -> id: $line"
    ssh -tt $line "sudo tc qdisc del dev ens3 root" &

    echo "server $i -> $line latency deleted"
    ((i++))
    if [[ $i -ge $1 ]]; then
	    break
	fi
done < serverlist
