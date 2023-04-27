#!/bin/bash

echo "$1"
var1=$(echo "from $2" | sha1sum)
var2=$(echo "to $3" | sha1sum)
var3=$(echo "date $4" | sha1sum)
echo -e -n "$var1\n$var2\n$var3" | shuf >> $1
