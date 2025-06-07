variable "project" {
  default = "url-checker-459813"
}

variable "region" {
  default = "us-west1"
}

variable "zone" {
  default = "us-west1-a"
}

variable "ssh_public_key_path" {
  type        = string
  description = "Ścieżka do pliku z kluczem publicznym SSH"
  default     = "~/.ssh/id_ed25519.pub"
}
