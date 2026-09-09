

# 2. Enable the Artifact Registry API (Required)
resource "google_project_service" "artifactregistry_api" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = true
}

# 3. Create the Docker Artifact Registry Repository
resource "google_artifact_registry_repository" "my_docker_repo" {
  location      = "europe-west1"
  repository_id = "my-docker-repo"
  description   = "Docker repository managed by Terraform"
  format        = "DOCKER"

  # Ensures API is fully enabled before creating the registry
  depends_on = [google_project_service.artifactregistry_api]
}

# 4. Output the Registry URL for CI/CD usage
output "repository_url" {
  value       = "${google_artifact_registry_repository.my_docker_repo.location}-docker.pkg.dev/${google_artifact_registry_repository.my_docker_repo.project}/${google_artifact_registry_repository.my_docker_repo.repository_id}"
  description = "The URL of the Docker repository"
}

