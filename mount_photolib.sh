#!/bin/sh
echo `pwd`/photos
mount -t nfs 192.168.1.7:/volume1/photo/PiFrame `pwd`/content
