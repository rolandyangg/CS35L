#!/bin/bash

# strategy is to hash whatever the thing is supp to be sort it, then sort the hashes f the other file and compare if they're equal

echo "$1"
var1=$(echo "from $2" | sha1sum)
var2=$(echo "to $3" | sha1sum)
var3=$(echo "date $4" | sha1sum)
verify=$(echo -e -n "$var1\n$var2\n$var3" | sort)
compare=$(sort file)

if [ "$verify" = "$compare" ]; then
	echo "SUCCESS"
else
	echo "FAIL"
fi

