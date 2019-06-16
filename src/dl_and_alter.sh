#!/bin/sh
# $1 video url


BINLOC=/usr/local/bin
LOGLOC=/var/log
PERSISTLOC=/etc/nflbot
SECLOC=$PERSISTLOC/secure
TEMPLOC=$PERSISTLOC/tmp
PYLIBLOC=/usr/local/lib/python3.5/dist-packages
DAEMONLOC=/etc/init.d





youtube-dl $1 --output $TEMPLOCK/og.mp4 --no-check-certificate --max-filesize 15M
ffmpeg -i $TEMPLOCK/og.mp4 -an -acodec copy $TEMPLOCK/og_deaf.mp4 -hide_banner -loglevel panic -nostats
ffmpeg -i $TEMPLOCK/og_deaf.mp4 -i $PERSISTLOC/NFL.mp3 -shortest -c:v copy -c:a aac -b:a 256k $TEMPLOCK/out.mp4 -hide_banner -loglevel panic -nostats
rm $TEMPLOCK/og.mp4
rm $TEMPLOCK/og_deaf.mp4