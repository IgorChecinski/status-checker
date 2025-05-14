provider "google" {
  credentials = file("credentials.json")
  project     = var.project
  region      = var.region
  zone        = var.zone
}

resource "google_compute_instance" "monitor" {
  name         = "monitor-instance"
  machine_type = "e2-micro"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network = "default"
    access_config {} # public IP
  }

  metadata_startup_script = file("startup.sh")
}
