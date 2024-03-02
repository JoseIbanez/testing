path "kv/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
path "kv/my-secret" {
  capabilities = ["read"]
}

