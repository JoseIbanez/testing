

apt-get update -y
apt-get install -y unzip
wget https://releases.hashicorp.com/consul/0.7.5/consul_0.7.5_linux_amd64.zip
unzip consul_0.7.5_linux_amd64.zip 
cp consul /usr/local/bin/
useradd consul
mkdir -p /etc/consul.d/{bootstrap,server,client}
mkdir /var/consul
chown consul:consul /var/consul



##bootstrap
cat > /etc/consul.d/bootstrap/config.json << EOF
{
    "bootstrap": true,
    "server": true,
    "datacenter": "nyc2",
    "data_dir": "/var/consul",
    "encrypt": "X4SYOinf2pTAcAHRhpj7dA==",
    "log_level": "INFO",
    "enable_syslog": true
}
EOF

##server
cat > /etc/consul.d/server/config.json << EOF
{
    "bootstrap": false,
    "server": true,
    "datacenter": "nyc2",
    "data_dir": "/var/consul",
    "encrypt": "X4SYOinf2pTAcAHRhpj7dA==",
    "log_level": "INFO",
    "enable_syslog": true,
    "start_join": ["10.226.135.27"]
}
EOF


cat > /etc/systemd/system/consul.service << EOF
[Unit]
Description=Consul agent server
Requires=network-online.target
After=network-online.target

[Service]
EnvironmentFile=-/etc/sysconfig/consul
Environment=GOMAXPROCS=2
Restart=on-failure
ExecStart=/usr/local/bin/consul agent $OPTIONS -config-dir=/etc/consul.d/server/config.json
ExecReload=/bin/kill -HUP $MAINPID
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
EOF
