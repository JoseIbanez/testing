# http://matt.dinham.net/juniper-vmx-getting-started-guide/


sudo apt-get upgrade
sudo apt-get install bridge-utils qemu-kvm libvirt-bin python python-netifaces vnc4server libyaml-dev python-yaml numactl libparted0-dev libpciaccess-dev libnuma-dev libyajl-dev libxml2-dev libglib2.0-dev libnl-dev python-pip python-dev libxml2-dev libxslt-dev
sudo reboot


sudo ./vmx.sh -lv --install


./vmx.sh --console vcp vmx1
