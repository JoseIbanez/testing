output "public_ip" {
  value = google_compute_instance.openwebui.network_interface[0].access_config[0].nat_ip
}

output "password" {
  sensitive = true
  value = random_password.password.result
}