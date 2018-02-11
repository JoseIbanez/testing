#!/bin/sh


sudo /usr/local/opt/openvpn/sbin/openvpn --config ~/.secrets/fra1.ovpn 


#https://www.cyberciti.biz/faq/linux-xen-vmware-kvm-intel-vt-amd-v-support/
dmesg | grep -i kvm



virt-install --name test --memory 1024 --disk /var/lib/glance/images/6419662b-3063-4f7c-a085-9964f6b8fa55 --import


virsh destroy vSRX
virsh undefine vSRX

virt-install --name vSRX --memory 4096 --cpu SandyBridge,+vmx,-invtsc --vcpus=2 \
        --arch=x86_64 \
        --graphics vnc,listen=0.0.0.0 --noautoconsole \
        --disk path=/tmp/media-srx-ffp-vsrx-vmdisk-15.1X49-D15.4.qcow2.old,size=16,device=disk,bus=ide,format=qcow2 \
        --os-type linux --os-variant rhel7 --import



cat <<EOF> /etc/libvirt/qemu/networks/default.xml
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



cat <<EOF> /etc/libvirt/qemu/networks/mgmt.xml
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

virsh net-define /etc/libvirt/qemu/networks/mgmt.xml
virsh net-start mgmt
virsh net-autostart mgmt

