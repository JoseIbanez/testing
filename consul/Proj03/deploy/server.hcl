#server.hcl

client_addr = "0.0.0.0"
data_dir = "/opt/consul"

server = true
bootstrap_expect = 3
ui_config {
   enabled = true
}

#bind_addr = "192.168.1.20"
#bind_addr = "{{ GetPrivateInterfaces | include \"network\" \"10.0.0.0/8\" | attr \"address\" }}"
#bind_addr = "{{ GetInterfaceIP \"eth0\" }}"

datacenter = "dc1"

encrypt = "f91X2S7GZic8EE+HGOw39b/LeFefz52UrPrVPvNdhqA="
ca_file = "/etc/consul.d/consul-agent-ca.pem"
cert_file = "/etc/consul.d/dc1-server-consul-0.pem"
key_file = "/etc/consul.d/dc1-server-consul-0-key.pem"

verify_incoming = true
verify_outgoing = true
verify_server_hostname = true

