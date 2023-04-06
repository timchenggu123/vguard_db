#!/bin/bash

i=1

read -p "---------- tests with catering factor $1 --------------"
while IFS= read -r line; do
    echo "starting host $i -> id: $line"
    ssh $line "cd go/src/vguard; ./vguard -id=0 -log=4 -r=0 -s=true -es=1 -b=1 -cfp=./config/cluster_4_cf_$i.conf -n=4 -m=32" &

    echo "server $i -> $line is done"
    ((i++))
    if [[ $i -ge $1 ]]; then
	    break
	fi
done < serverlist

$i=1
$j=1

read -p "---------- starting 2 followers on each server ------------"
while IFS= read -r line; do
	echo "starting followers $i -> id: $line"
	ssh -T $line <<'EOL'
		cd go/src/vguard
		j=1
		while $j -le $1; do
			./vguard -id=
		done
EOL
done < serverlist
