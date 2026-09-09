terraform {
  required_providers {
    google = {
       source = "hashicorp/google"
       version = "6.0.1"
    }   

    terracurl = {
      source  = "devops-rob/terracurl"
      version = "2.3.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "3.6.2"
    }


  }

}


provider "google" {
}

provider "terracurl" {
}

provider "random" {
}


variable "open_webui_user" {
  description = "Username for Open Web UI"
  default     = "admin@demo.gs"  
}

variable "openai_base" {
  description = "OpenAI Base URL"
  default     = "https://api.openai.com/v1"
}

variable "openai_key" {
  description = "Optional OpenAI API Key"
  default     = ""
}

variable "machine" {
  description = "The machine type and image to use for the VM"
  # GPU instance with 24GB of memory and 4 vCPUs with 16GB of system RAM
  default = {
    "gpu" : { "type" : "g2-standard-4", "project" : "click-to-deploy-images", "family" : "common-cu121-debian-11-py310" }
    "cpu" : { "type" : "n1-standard-4", "project" : "debian-cloud", "family" : "debian-11" }
  }
}

variable "gpu_enabled" {
  description = "Enable GPU support"
  default     = false
}