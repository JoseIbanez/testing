provider "aws" {
  region     = "eu-central-1"
}

resource "aws_instance" "web" {
  count           = 3
  ami             = "ami-1e339e71"
  instance_type   = "t2.nano"
  key_name        = "kumo"
  security_groups = ["mgmt"]


  tags {
    Name = "${format("web-%03d", count.index + 1)}"
    Name_old = "web-${count.index}"

  }
}

