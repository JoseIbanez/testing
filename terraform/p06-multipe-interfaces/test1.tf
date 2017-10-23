provider "aws" {
  region     = "us-east-2"
}

resource "aws_instance" "j1" {
  ami           = "ami-00230365"
  instance_type = "m4.xlarge"
  key_name      = "junos_ohio"
  #security_groups = ["mgmt"]
  availability_zone = "us-east-2b"

  tags {
    Name = "j1"
  }
}

resource "aws_network_interface" "test" {
  subnet_id       = "subnet-0d77ce76"

  attachment {
    instance     = "${aws_instance.j1.id}"
    device_index = 1
  }
}