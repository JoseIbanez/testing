ffmpeg -r 10 \
    -f image2 -s 1920x1080 \
    -start_number 547 -i Y007%04d.jpg  \
    -vcodec libx264 -crf 25  -pix_fmt yuv420p \
    test.mp4

