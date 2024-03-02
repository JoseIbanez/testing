// Enable UI
ui = true

// Filesystem storage
storage "file" {
  path = "./vault-volume"
}

// TCP Listener
listener "tcp" {
  address = "0.0.0.0:8201"
  tls_disable = "true"
}