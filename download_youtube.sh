#!/bin/bash
cat list/all | awk '{print $1}' > list/all.video
for line in $(cat "list/all.video"); do
    ytdl -b "http://www.youtube.com/watch?v=${line}"
done