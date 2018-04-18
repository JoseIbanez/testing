ffmpeg -r 24 \
    -f image2 -s 1920x1080 \
    -start_number 1162 -i Y009%04d.jpg  \
    -vcodec libx264 -crf 25  -pix_fmt yuv420p \
    ~/Movies/tl-20180402.10fps.mp4
