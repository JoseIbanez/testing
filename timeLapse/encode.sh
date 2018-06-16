------------------------------

ffmpeg -r 24 \
    -f image2 -s 1920x1080 \
    -start_number 1162 -i Y009%04d.jpg  \
    -vcodec libx264 -crf 25  -pix_fmt yuv420p \
    ~/Movies/tl-20180402.10fps.mp4


-------------------

ffmpeg -r 20 \
    -f image2 -s 1920x1080 \
    -start_number 0888 \
    -i Y014%04d.jpg  \
    -vcodec libx264 -crf 25  -pix_fmt yuv420p \
    ~/Movies/tl-20180428.20fps.mp4


-------------------



# 20 fps, NikonA300 folder

ffmpeg -r 20 \
    -f image2 -s 1920x1080 \
    -start_number 4101 -i DSCN%04d.jpg  \
    -vcodec libx264 -crf 25  -pix_fmt yuv420p \
    ~/Movies/tl-20180429.20fps.mp4
