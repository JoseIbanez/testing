provider "aws" {
  region     = "eu-central-1"
}

resource "aws_instance" "web-1" {
  ami           = "ami-1e339e71"
  instance_type = "t2.micro"
  key_name      = "kumo"
  security_groups = ["mgmt"]

  tags {
    Name = "web-2"
  }
}

resource "aws_instance" "web-2" {
  ami           = "ami-1e339e71"
  instance_type = "t2.micro"
  key_name      = "kumo"
  security_groups = ["mgmt"]

  tags {
    Name = "web-2"
  }

}
