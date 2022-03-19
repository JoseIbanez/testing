

consul keygen > consul-encrypt-key.txt
consul tls ca create

consul tls cert create -server -dc dc1
consul tls cert create -client -dc dc1

scp \
    consul-agent-ca.pem \
    dc1-server-consul-0.pem \
    dc1-server-consul-0-key.pem \
    <user>@<server>:/etc/consul.d/

