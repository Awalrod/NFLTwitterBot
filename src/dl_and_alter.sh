#!/bin/sh
# $1 video url




ARTIFACT="untracked/artifacts"




youtube-dl $1 --output $ARTIFACT/og.mp4 --no-check-certificate
ffmpeg -i $ARTIFACT/og.mp4 -an -acodec copy $ARTIFACT/og_deaf.mp4
ffmpeg -i $ARTIFACT/og_deaf.mp4 -i src/NFL.mp3 -shortest -c:v copy -c:a aac -b:a 256k $ARTIFACTout.mp4
rm $ARTIFACT/og.mp4
rm $ARTIFACT/og_deaf.mp4