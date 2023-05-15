

export ACE_URL="http://ott-cdn.ucom.am/s24/04.m3u8"

ffmpeg  -headers 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en-us,en;q=0.5
Range:  
' -i $ACE_URL \
 -c copy -map 0 \
 -f hls \
 -hls_list_size 20 -hls_delete_threshold 3 -hls_flags delete_segments \
 -hls_init_time 4 -hls_time 4 \
 stream.m3u8




export ACE_URL="https://vs-hls-push-uk-live.akamaized.net/x=3/i=urn:bbc:pips:service:bbc_one_hd/t=3840/v=pv14/b=5070016/main.m3u8"
export ACE_URL="https://vs-hls-push-uk-live.akamaized.net/x=3/i=urn:bbc:pips:service:bbc_two_hd/t=3840/v=pv14/b=5070016/main.m3u8"
export ACE_URL="http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_london.m3u8"

export ACE_URL="http://vs-hls-uk-live.akamaized.net/pool_902/live/uk/bbc_one_london/bbc_one_london.isml/bbc_one_london-pa3%3d96000-video%3d1604032.norewind.m3u8"


ffmpeg  \
 -i $ACE_URL \
 -c copy -map 0 \
 -f hls \
 -hls_list_size 20 -hls_delete_threshold 3 -hls_flags delete_segments \
 -hls_init_time 4 -hls_time 4 \
 stream.m3u8



rm *.ts *.m3u8
tsprefix=`date +%d%H%M`

ffmpeg \
 -reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -re  \
 -i $ACE_URL \
 -map 0:v:0 -map 0:a:0 \
 -c:v copy \
 -c:a ac3 \
 -f hls \
 -hls_list_size 20 -hls_delete_threshold 3 -hls_flags delete_segments \
 -hls_segment_filename "d${tsprefix}stream%d.ts" \
 -hls_init_time 4 -hls_time 4 \
 stream.m3u8

 


