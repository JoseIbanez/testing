

docker run -d --name acelink -p 6878:6878 blaiseio/acelink



hls acestream://5817f9d710d682fe975a16c47306bfdced437319 #BT sports KO
hls acestream://3484a8b98af044d885fdc5f77e6e46a1506cbcf6 #Movistar Champions
hls acestream://5817f9d710d682fe975a16c47306bfdced437319 #BT SPORT 2 FHD
hls acesteram://725ae2bab937292731246f620f1e84d353f64d19 #ArenaVision 3
hls acesteram://a7df83def680c57ea9f67271ddf10c61266695a6 #ArenaVision 13
hls acesteram://da465079d5b418a3cac268314dd0b39cb28c88e7

vlc http://192.168.1.20:8800/3231/stream.m3u8




######

rm -f *.ts
rm -f *.m3u8

#export ACE_URL="http://127.0.0.1:6878/ace/manifest.m3u8?id=$ID"
export ACE_URL="http://127.0.0.1:6878/ace/getstream?id=$ID"

ffmpeg \
 -i $ACE_URL \
 -c copy -map 0 \
 -f hls \
 -hls_list_size 20 -hls_delete_threshold 3 -hls_flags delete_segments \
 -hls_init_time 4 -hls_time 4 \
 stream.m3u8
