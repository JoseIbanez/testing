provider "aws" {
  region     = "us-east-2"
}


data "aws_subnet" "pub" {

  filter {
    name = "tag:Name"
    values = ["Pub"]
  }

}


data "aws_subnet" "pri_a" {

  filter {
    name = "tag:Name"
    values = ["Private A"]
  }

}


output "subnet_pub" {
  value = "${data.aws_subnet.pub.id}"
}

output "subnet_pri_a" {
  value = "${data.aws_subnet.pri_a.id}"
}


resource "aws_instance" "j1" {
  ami               = "ami-c5062ba0"
  #ami              = "ami-00230365"
  #instance_type    = "m4.xlarge"
  instance_type     = "t2.nano"
  key_name          = "junos_ohio"
  #security_groups  = ["mgmt"]
  availability_zone = "us-east-2b"
  subnet_id         = "${data.aws_subnet.pub.id}" 

  tags {
    Name = "j1"
  }

}

resource "aws_network_interface" "test" {
  subnet_id       = "${data.aws_subnet.pri_a.id}"

  attachment {
    instance     = "${aws_instance.j1.id}"
    device_index = 1
  }
}