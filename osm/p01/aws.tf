provider "aws" {
  region     = "eu-central-1"
}



resource "aws_volume_attachment" "ebs_att" {
  device_name = "/dev/sdh"
  volume_id   = "${aws_ebs_volume.vol1.id}"
  instance_id = "${aws_instance.kumo.id}"
  skip_destroy = true
}


resource "aws_ebs_volume" "vol1" {
  availability_zone = "eu-central-1a"
  size              = 100
}


resource "aws_instance" "kumo" {
  ami               = "ami-1e339e71"
  instance_type     = "t2.xlarge"
  key_name          = "kumo"
  security_groups   = ["mgmt"]
  availability_zone = "eu-central-1a"

  tags {
    Name = "kumo10"
  }
}
