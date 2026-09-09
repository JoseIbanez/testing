resource "random_password" "password" {
  length  = 16
  special = true
}

resource "google_service_account" "openwebui" {
  account_id   = "openwebui"
  display_name = "Custom SA for OpenWebUI VM Instance"
}

data "google_compute_image" "debian" {
  family  = "debian-12"
  project = "debian-cloud"
}

resource "google_compute_instance" "openwebui" {
  name         = "openwebui"
  machine_type = "e2-medium" # "n2-standard-4"
  zone         = "europe-west1-b"

  tags = ["ssh","http"]

  boot_disk {
    initialize_params {
      image = data.google_compute_image.debian.self_link
      size = 200
    }
  }


  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }

  metadata_startup_script = templatefile(
    "${path.module}/scripts/provision_vars.sh", 
    {
        open_webui_user = var.open_webui_user
        open_webui_password = random_password.password.result
        openai_base     = var.openai_base
        openai_key      = var.openai_key
        gpu_enabled     = var.gpu_enabled
    })

  metadata = {
    ssh-keys = "openwebui:${file("~/.ssh/id_rsa.pub")}"
  }


  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.openwebui.email
    scopes = ["cloud-platform"]
  }
}

resource "google_compute_firewall" "openwebui_ssh" {
  name    = "openwebui-ssh"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags   = ["ssh"]
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "openwebui_http" {
  name    = "openwebui-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  target_tags   = ["http"]
  source_ranges = ["0.0.0.0/0"]
}



resource "terracurl_request" "openwebui" {
  method = "GET"
  name = "openwebui"
  url = "http://${google_compute_instance.openwebui.network_interface[0].access_config[0].nat_ip}:80"
  timeout = 10

  response_codes = [200]
  max_retry = 20
  retry_interval = 10
}
