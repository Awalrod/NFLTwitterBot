#!/bin/sh
BINLOC=/usr/local/bin
LOGLOC=/var/log
PERSISTLOC=/etc/nflbot
SECLOC=$PERSISTLOC/secure
TEMPLOC=$PERSISTLOC/tmp
PYLIBLOC=/usr/local/lib/python3.5/dist-packages
DAEMONLOC=/etc/init.d

rm -rf $TEMPLOC/*
