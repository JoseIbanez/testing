#consul.hcl

client_addr = "0.0.0.0"
data_dir = "/opt/consul"

datacenter = "dc1"

encrypt = "f91X2S7GZic8EE+HGOw39b/LeFefz52UrPrVPvNdhqA="
ca_file = "/etc/consul.d/consul-agent-ca.pem"
cert_file = "/etc/consul.d/dc1-agent-consul-0.pem"
key_file = "/etc/consul.d/dc1-agent-consul-0-key.pem"

