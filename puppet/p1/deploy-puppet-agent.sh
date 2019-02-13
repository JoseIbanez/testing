

apt-get update -y
apt-get install -y puppet



cat > /etc/puppet/puppet.conf <<EOF
[main]
ssldir = /var/lib/puppet/ssl

[agent]
server = m1
EOF

cat >> /etc/hosts <<EOF
10.4.76.1 m1 puppet
EOF

service puppet stop
service puppet start

tail -f /var/log/syslog 

