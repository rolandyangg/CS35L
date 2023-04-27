#!/bin/bash

# for checking...
# pstree -U $USER

BASHPROCESS=$(ps -o ppid= -p $$)
SSHPROCESS=$(ps -o ppid= -p $BASHPROCESS)
LOGINPROCESS=$(ps -o ppid= -p $SSHPROCESS)

# each process should only have one ancestor theoretically but check for multiple just in case...
function getAncestors {
    ancestors=$(ps -o ppid= -p $1)
    for x in $ancestors; do
	if [ $x != 0 ]
	then
	    ps -f --no-headers $x
	    getAncestors $x
        fi
    done
}

function getDescendants {
    descendants=$(ps -o pid= --ppid $1)
    for x in $descendants; do
	ps -f --no-headers $x
	getDescendants $x
    done
}

echo "login process: "
ps -f --no-headers $LOGINPROCESS
echo

echo "ancestors: "
getAncestors $LOGINPROCESS
echo

echo "descendants: "
getDescendants $LOGINPROCESS
echo
