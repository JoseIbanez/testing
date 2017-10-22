provider "aws" {
  region     = "${var.region}"
}


### VPC creation
################

resource "aws_vpc" "vpc" {
  cidr_block       = "10.0.0.0/16"
  tags {
    Name = "iba"
  }
}

### Subnet creation
#
# Pub: MGMT, VPN
# PriA 
# PriB


resource "aws_subnet" "pub_subnet" {
  availability_zone = "${var.zone}"
  vpc_id  = "${aws_vpc.vpc.id}"
  cidr_block = "10.0.0.0/24"
  map_public_ip_on_launch = true

  tags {
    Name = "Pub"
  }
}

resource "aws_subnet" "pri_a_subnet" {
  availability_zone = "${var.zone}"
  vpc_id  = "${aws_vpc.vpc.id}"
  cidr_block = "10.0.1.0/24"

  tags {
    Name = "Private A"
  }
}

resource "aws_subnet" "pri_b_subnet" {
  availability_zone = "${var.zone}"
  vpc_id  = "${aws_vpc.vpc.id}"
  cidr_block = "10.0.2.0/24"

  tags {
    Name = "Private B"
  }
}

### Output

output "vpc" {
  value = "${aws_vpc.vpc.id}"
}

output "subnet_pub" {
  value = "${aws_subnet.pub_subnet.id}"
}

output "subnet_pri_a" {
  value = "${aws_subnet.pri_a_subnet.id}"
}

output "subnet_pri_b" {
  value = "${aws_subnet.pri_b_subnet.id}"
}

##############################
# Route route table


#main_route_table_id

resource "aws_route" "p" {
  route_table_id            = "${aws_vpc.vpc.main_route_table_id}"
  destination_cidr_block    = "0.0.0.0/0"
  gateway_id                = "${aws_internet_gateway.igw.id}"
}


resource "aws_route_table_association" "p" {
  subnet_id      = "${aws_subnet.pub_subnet.id}"
  route_table_id = "${aws_vpc.vpc.main_route_table_id}"

}


resource "aws_route_table" "pri_a" {
  vpc_id = "${aws_vpc.vpc.id}"
  tags {
    Name = "Private A"
  }
}

resource "aws_route_table_association" "a1" {
  subnet_id      = "${aws_subnet.pri_a_subnet.id}"
  route_table_id = "${aws_route_table.pri_a.id}"
}


resource "aws_route_table" "pri_b" {
  vpc_id = "${aws_vpc.vpc.id}"
  tags {
    Name = "Private B"
  }
}

resource "aws_route_table_association" "a2" {
  subnet_id      = "${aws_subnet.pri_b_subnet.id}"
  route_table_id = "${aws_route_table.pri_b.id}"
}


output "rt_pri_a" {
  value = "${aws_route_table.pri_a.id}"
}

output "rt_pri_b" {
  value = "${aws_route_table.pri_b.id}"
}


####################################
# Internet GW

resource "aws_internet_gateway" "igw" {
  vpc_id = "${aws_vpc.vpc.id}"

  tags {
    Name = "iba"
  }
}

