#!/bin/bash
set -e

# --- Wczytanie zmiennych ze .env, jeśli plik istnieje ---
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
  echo "Loaded environment variables from .env"
else
  echo "Warning: .env file not found. Make sure SSH_KEY_PATH is set in environment."
fi

# --- Rozwiń ~ w ścieżce klucza SSH jeśli jest ---
if [[ "$SSH_KEY_PATH" == ~* ]]; then
  SSH_KEY_PATH="${SSH_KEY_PATH/#\~/$HOME}"
fi

# --- Sprawdzenie, czy zmienna SSH_KEY_PATH jest ustawiona ---
if [ -z "$SSH_KEY_PATH" ]; then
  echo "Error: SSH_KEY_PATH is not set. Please set it in .env or as environment variable."
  exit 1
fi

# --- Sprawdzenie, czy plik klucza SSH istnieje ---
if [ ! -f "$SSH_KEY_PATH" ]; then
  echo "Error: SSH key file not found at '$SSH_KEY_PATH'."
  exit 1
fi

# --- Krok 1: Uruchom terraform apply ---
echo "▶️ Applying Terraform..."
cd infra
terraform apply -auto-approve

# --- Krok 2: Pobierz IP maszyny z output Terraform ---
echo "🌐 Fetching VM IP from Terraform output..."
INSTANCE_IP=$(terraform output -raw instance_ip)

if [ -z "$INSTANCE_IP" ]; then
  echo "Error: Could not fetch VM IP from Terraform output."
  exit 1
fi

# --- Krok 3: Wygeneruj inventory dla Ansible ---
echo "🛠️ Generating Ansible inventory..."
cat <<EOF > ../provisioning/inventory.ini
[vm]
$INSTANCE_IP ansible_user=ubuntu ansible_ssh_private_key_file=${SSH_KEY_PATH}
EOF

# --- Krok 4: Uruchom Ansible playbook ---
echo "🚀 Running Ansible playbook..."
cd ../provisioning
ansible-playbook -i inventory.ini playbook.yml

echo "✅ Provisioning completed successfully!"
