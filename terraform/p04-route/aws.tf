provider "aws" {
  region     = "eu-central-1"
}



resource "aws_instance" "kumo1" {
  ami               = "ami-1e339e71"
  instance_type     = "t2.nano"
  key_name          = "kumo"
#  security_groups   = ["mgmt"]
  subnet_id         = "subnet-dbcf04b0" # subnet: pri_01 
  availability_zone = "eu-central-1a"

  tags {
    Name = "kumo01"
  }

}
#eni-59f1d90b


resource "aws_instance" "kumo2" {
  ami               = "ami-1e339e71"
  instance_type     = "t2.nano"
  key_name          = "kumo"
#  security_groups  = ["mgmt"]
  subnet_id         = "subnet-63c80308" # subnet: pri_02
  availability_zone = "eu-central-1a"

  tags {
    Name = "kumo02"
  }

}


resource "aws_route" "r-01" {
  route_table_id  = "rtb-1c499d77"
  destination_cidr_block = "99.99.0.1/32"
  network_interface_id  = "${aws_instance.kumo2.network_interface_id}"
}


