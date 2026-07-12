resource "google_service_account" "openwebui" {
  account_id   = "openwebui"
  display_name = "Custom SA for VM Instance"
}

data "google_compute_image" "debian" {
  family  = "debian-11"
  project = "debian-cloud"
}


resource "google_compute_instance" "openwebui" {
  name         = "openwebui"
  machine_type = "n2-standard-4"
  zone         = "europe-west1-b"

  tags = ["ssh"]

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

  metadata = {
    ssh-keys = "openwebui:${file("~/.ssh/id_rsa.pub")}"
  }

  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.openwebui.email
    scopes = ["cloud-platform"]
  }
}



resource "google_compute_firewall" "openwebui" {
  name    = "openwebui"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags = ["ssh"]
  source_ranges = ["0.0.0.0/0"]
}