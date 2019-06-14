#!/bin/sh
# $1 video url




ARTIFACT="untracked/artifacts"




youtube-dl $1 --output $ARTIFACT/og.mp4 --no-check-certificate --max-filesize 15M
ffmpeg -i $ARTIFACT/og.mp4 -an -acodec copy $ARTIFACT/og_deaf.mp4 -hide_banner -loglevel panic -nostats
ffmpeg -i $ARTIFACT/og_deaf.mp4 -i src/NFL.mp3 -shortest -c:v copy -c:a aac -b:a 256k $ARTIFACT/out.mp4 -hide_banner -loglevel panic -nostats
rm $ARTIFACT/og.mp4
rm $ARTIFACT/og_deaf.mp4