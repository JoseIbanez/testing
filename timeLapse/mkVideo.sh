#!/bin/bash
# 20 fps, NikonA300 folder

prefix="DSCN"
rate="40"


start=$1

if [ -n "$2" ] ; then
   rate=$2
fi

if [ -n "$3" ] ; then
  prefix=$3
fi

echo $start
echo $rate
echo $prefix

#exit

#ffmpeg -r $rate \
#    -f image2 -s 1920x1080 \
#    -start_number $start -i $prefix%04d.JPG  \
#    -vcodec libx264 -crf 25  -pix_fmt yuv420p \
#    ~/Movies/tl-$start.$rate.fps.mp4


ffmpeg -r $rate \
    -f image2 -s 1920x1080 \
    -start_number $start -i $prefix%04d.JPG  \
    -c:v libx264 -profile:v baseline -level 3.0 \
    -pix_fmt yuv420p \
    ~/Movies/tl-$start.$rate.fps.mp4

