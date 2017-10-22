provider "aws" {
  region     = "${var.region}"
}

module "vpc" {
  source = "./modules/vpc"
  region = "${var.region}"
  zone   = "${var.zone}"
}


resource "aws_instance" "kumo1" {
  ami               = "ami-c5062ba0"
  instance_type     = "t2.nano"
  key_name          = "junos_ohio"
#  security_groups   = ["mgmt"]
  subnet_id         = "${module.vpc.subnet_pub}" 
  availability_zone = "${var.zone}"

  tags {
    Name = "kumo01"
  }

}
#eni-59f1d90b

