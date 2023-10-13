docker run \
    -e JVM_XMX=256m \
    -v i2phome:/i2p/.i2p \
    -v i2ptorrents:/i2psnark \
    -p 4444:4444 \
    -p 6668:6668 \
    -p 7657:7657 \
    -p 54321:12345 \
    -p 54321:12345/udp \
    i2p:latest
