# shellcheck disable=SC2046
kill -9 $(ps aux | grep 'vguard' | awk '{print $2}')

# kill process by the port number
fuser -k ${1:-11000}/tcp

# remove tasks in AT queue
for i in $(atq | cut -f 1); do
	atrm $i
done
