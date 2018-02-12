#!/bin/sh


sudo /usr/local/opt/openvpn/sbin/openvpn --config ~/.secrets/fra1.ovpn 


#https://www.cyberciti.biz/faq/linux-xen-vmware-kvm-intel-vt-amd-v-support/
dmesg | grep -i kvm


https://www.juniper.net/documentation/en_US/vsrx/topics/task/multi-task/security-vsrx-with-kvm-installing.html#jd0e230


cat /sys/module/kvm_intel/parameters/nested 

sudo rmmod kvm-intel
sudo sh -c "echo 'options kvm-intel nested=y enable_apicv=n pml=n' >> /etc/modprobe.d/dist.conf"
sudo modprobe kvm-intel


virt-install --name test --memory 1024 \
        --graphics vnc,listen=0.0.0.0 --noautoconsole \
        --disk /var/lib/libvirt/images/c1.img --import


virsh destroy vSRX
virsh undefine vSRX

virt-install --name vSRX --memory 4096 --cpu SandyBridge,+vmx,-invtsc --vcpus=2 \
        --arch=x86_64 \
        --graphics vnc,listen=0.0.0.0 --noautoconsole \
        --disk path=/var/lib/libvirt/images/j1.qcow2,size=16,device=disk,bus=ide,format=qcow2 \
        --os-type linux --os-variant rhel7 --import


virt-install --name vSRX --memory 4096 --cpu Westmere,+vmx,-invtsc --vcpus=2 \
        --arch=x86_64 \
        --graphics vnc,listen=0.0.0.0 --noautoconsole \
        --disk path=/var/lib/libvirt/images/j1.qcow2,size=16,device=disk,bus=ide,format=qcow2 \
        --os-type linux --os-variant rhel7 --import


  <cpu mode='custom' match='exact' check='partial'>
    <model fallback='allow'>SandyBridge</model>
    <vendor>Intel</vendor>
    <feature policy='require' name='vmx'/>
    <feature policy='disable' name='x2apic'/>
    <feature policy='disable' name='invtsc'/>
  </cpu>
  <graphics type='vnc' port='-1' autoport='yes'  listen='127.0.0.1' passwd='1234'/>


cat <<EOF > /etc/libvirt/qemu/networks/default.xml
<network>
<name>default</name>
<forward mode='nat'/>
<nat>
<port start ='1024' end='65535' />
</nat>
<bridge name='virbr0' stp='on' delay='0' />
<ip address='192.168.2.1' netmask='255.255.255.0'>
<dhcp>
<range start='192.168.2.2' end='192.168.2.254' />
</dhcp>
</ip>
</network>
EOF

virsh net-define /etc/libvirt/qemu/networks/default.xml
virsh net-start default
virsh net-autostart default



cat <<EOF > /etc/libvirt/qemu/networks/mgmt.xml
<network>
<name>mgmt</name>
<forward mode='nat'/>
<nat>
<port start ='1024' end='65535' />
</nat>
<bridge name='virbr1' stp='on' delay='0' />
<ip address='10.39.10.1' netmask='255.255.255.0'>
<dhcp>
<range start='10.39.10.50' end='10.39.10.254' />
</dhcp>
</ip>
</network>
EOF


cat <<EOF > /etc/libvirt/qemu/networks/mgmt.xml
<network>
<name>mgmt</name>
<forward mode='route'/>
<bridge name='virbr1' stp='on' delay='0' />
<ip address='10.39.10.1' netmask='255.255.255.0'>
<dhcp>
<range start='10.39.10.50' end='10.39.10.254' />
</dhcp>
</ip>
</network>
EOF



virsh net-define /etc/libvirt/qemu/networks/mgmt.xml
virsh net-start mgmt
virsh net-autostart mgmt


virsh list
virsh destroy vSRX
virsh update-device vSRX change-pwd.xml 
virsh dumpxml --security-info vSRX | grep grap
virsh start vSRX
virsh dumpxml --security-info vSRX | grep grap
