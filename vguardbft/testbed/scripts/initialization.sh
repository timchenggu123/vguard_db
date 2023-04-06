#!/bin/bash

i=0

while IFS= read -r line; do
	echo "ssh-keygen to server $i on host -> id: $line"
	ssh-keygen -R $line

	echo "copying serverlist to server $i"
	scp ./serverlist $line:~/go/src/vguard
	
	echo "ssh-keygen on server $i"
	ssh -T $line <<'EOL'
		cd go/src/vguard
		cp ./serverlist ./scripts/serverlist
		j=0
		while IFS= read -r sline; do
			ssh-keygen -R $sline
			((j++))
		done < serverlist
EOL
	echo "server $i -> $line is done"
	((i++))
done < serverlist
