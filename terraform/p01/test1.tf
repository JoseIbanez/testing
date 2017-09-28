provider "aws" {
  region     = "eu-central-1"
}

resource "aws_instance" "example" {
  ami           = "ami-1e339e71"
  instance_type = "t2.micro"
  key_name      = "kumo"
  security_groups = ["mgmt"]
}
