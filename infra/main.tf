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

  service_account {
    email  = google_service_account.vm_sa.email
    scopes = ["https://www.googleapis.com/auth/devstorage.read_write"]
  }

  metadata_startup_script = file("startup.sh")
}

resource "google_storage_bucket" "backup_bucket" {
  name          = "${var.project}-backup-bucket"
  location      = var.region
  force_destroy = true # usuwa bucket nawet jeśli są w nim pliki

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 # usuń pliki starsze niż 30 dni
    }
  }
}

resource "google_service_account" "vm_sa" {
  account_id   = "monitor-vm-sa"
  display_name = "Service account for monitor VM"
}

resource "google_storage_bucket_iam_member" "allow_vm_write" {
  bucket = google_storage_bucket.backup_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.vm_sa.email}"
}
