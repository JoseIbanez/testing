# -*- mode: ruby -*-
# vi: set ft=ruby :

# check with: ulimit -n 4048

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/bionic64"
  #config.vm.box = "ubuntu/focal64"
  #config.vm.box = "bento/ubuntu-20.04"

  config.vm.define "m1" do |m1|
      #m1.vm.provision "shell", path: "./deploy-01.sh"
      m1.vm.hostname = "m1"
      #m1.vm.synced_folder ".", "/vagrant", type: 'virtualbox'
      m1.vm.network "forwarded_port", guest: 8888, host: 8888
      m1.vm.network "forwarded_port", guest: 8080, host: 8080
      m1.vm.network "forwarded_port", guest: 8082, host: 8082
      m1.vm.network "forwarded_port", guest: 5000, host: 5000
      m1.vm.network "forwarded_port", guest: 15672, host: 15672
      #m1.vm.network "private_network", ip: "192.168.58.11", virtualbox__intnet: "vboxnet2"
  end


  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "2048"]
    vb.customize ["modifyvm", :id, "--cpus", "2"]
    #vb.customize ["modifyvm", :id, "--cpuexecutioncap", "80"]

  end

end
