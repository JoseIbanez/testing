# -*- mode: ruby -*-
# vi: set ft=ruby :

# check with: ulimit -n 4048

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  #config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  #config.vm.box = "trusty64"
  config.vm.box = "ubuntu/xenial64"


  config.vm.define "m1" do |m1|
      #m1.vm.provision "shell", path: "./deploy-01.sh"
      m1.vm.hostname = "m1"
      #m1.vm.network "private_network", ip: "172.20.20.11"
      m1.vm.network "public_network", ip: "192.168.1.30"
  end


  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
    vb.customize ["modifyvm", :id, "--cpus", "2"]
    vb.customize ["modifyvm", :id, "--cpuexecutioncap", "80"]
  end

end
