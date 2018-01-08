provider "aws" {
  region     = "eu-central-1"
}






resource "aws_instance" "kube00" {
  ami           = "ami-1e339e71"
  instance_type = "t2.large"
  key_name      = "kumo"
  security_groups = ["mgmt"]
  availability_zone = "eu-central-1a"


  tags {
    Name = "kube00"
  }
}

resource "aws_instance" "kube01" {
  ami           = "ami-1e339e71"
  instance_type = "t2.large"
  key_name      = "kumo"
  security_groups = ["mgmt"]
  availability_zone = "eu-central-1a"


  tags {
    Name = "kube01"
  }
}

resource "aws_instance" "kube02" {
  ami           = "ami-1e339e71"
  instance_type = "t2.large"
  key_name      = "kumo"
  security_groups = ["mgmt"]
  availability_zone = "eu-central-1a"


  tags {
    Name = "kube02"
  }
}

