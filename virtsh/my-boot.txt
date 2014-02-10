#!/bin/sh
echo "Hello World!"
echo "This will run as soon as possible in the boot sequence"

cat > /etc/apt/apt.conf.d/88apt-proxy << EOF
Acquire::http::Proxy "http://192.168.1.30:8000";
EOF

apt-get update
apt-get upgrade -y
apt-get install -y atop
