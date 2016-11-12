#!/bin/bash

mkdir $2

for f in "$1"
	do midi2abc -ga -gk "$f" -o "$2/$f.abc"
done

rename ".mid.abc" ".abc" "$2/*"
