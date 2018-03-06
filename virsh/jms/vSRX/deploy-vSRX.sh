virsh destroy vSRX
virsh undefine vSRX

https://www.juniper.net/documentation/en_US/vsrx/topics/task/multi-task/security-vsrx-with-kvm-installing.html#jd0e230

https://mattillingworth.wordpress.com/2016/02/04/vsrx-15-1-problems/

cp /mnt/images-repo/media-srx-ffp-vsrx-vmdisk-15.1X49-D15.4.qcow2 /var/lib/libvirt/images/j2.qcow2

#virt-install --name j2 --memory 4096 --cpu SandyBridge,+vmx,-invtsc --vcpus=2 ...
virt-install --name j2 --memory 4096 --cpu SandyBridge,+vmx,-invtsc,-x2apic --vcpus=2 \
        --arch=x86_64 \
        --graphics vnc,listen=0.0.0.0 --noautoconsole \
        --disk path=/var/lib/libvirt/images/j2.qcow2,size=16,device=disk,bus=ide,format=qcow2 \
        --os-type linux --os-variant rhel7 \
        --network=network:mgmt,model=virtio \
        --network=network:wan1101,model=virtio \
        --network=network:wan1102,model=virtio \
        --import

virt-install --name j2 --memory 4096 --cpu SandyBridge,+vmx,-invtsc --vcpus=2 \
        --arch=x86_64 \
        --graphics vnc,listen=0.0.0.0 --noautoconsole \
        --disk path=/var/lib/libvirt/images/j2.qcow2,size=16,device=disk,bus=ide,format=qcow2 \
        --os-type linux --os-variant rhel7 \
        --network=network:vmMgmt,model=virtio \
        --network=network:vmMgmt,model=virtio \
        --network=network:vmMgmt,model=virtio \
        --import



sudo virsh dumpxml --security-info  j2 | grep graphics
sudo virsh update-device j2 ./vnc.xml 
sudo virsh dumpxml --security-info  j2 | grep graphics

virsh domiflist j2




virt-install --name vSRX20One --ram 4096 \
--cpu SandyBridge,+vmx,-invtc, --vcpus=2 --arch=x86_64 \
--disk path=/mnt/vsrx20one.qcow2,size=16,device=disk,bus=ide,format=qcow2 \
--os-type linux --os-variant rhel7 \
--import \
--network=network:default,model=virtio \
--network=network:TestLeft,model=virtio \
--network=network:TestRight,model=virtio



  <cpu mode='custom' match='exact' check='partial'>
    <model fallback='allow'>SandyBridge</model>
    <vendor>Intel</vendor>
    <feature policy='require' name='vmx'/>
    <feature policy='disable' name='x2apic'/>
    <feature policy='disable' name='invtsc'/>
  </cpu>

  <graphics type='vnc' port='-1' autoport='yes'  listen='127.0.0.1' passwd='1234'/>

    <interface type='network'>
      <mac address='52:54:00:69:20:63'/>
      <source network='mgmt' bridge='virbr1'/>
      <target dev='vnet0'/>
      <model type='rtl8139'/>
      <alias name='net0'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
    </interface>

    <interface type='network'>
      <source network='wan1101'/>
      <target dev='ge-000-j2'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
    </interface>




#17.3R2
cp /mnt/images-repo/media-vsrx-vmdisk-17.3R2.10.qcow2 /var/lib/libvirt/images/j2.qcow2


virt-install --name j2 --memory 4096 --cpu SandyBridge,+vmx,-invtsc --vcpus=2 \
        --arch=x86_64 \
        --graphics vnc,listen=0.0.0.0 --noautoconsole \
        --disk path=/var/lib/libvirt/images/j2.qcow2,size=16,device=disk,bus=ide,format=qcow2 \
        --os-type linux --os-variant rhel7 \
        --network=network:vmMgmt,model=virtio \
        --network=network:vmMgmt,model=virtio \
        --network=network:vmMgmt,model=virtio \
        --import


sudo virsh destroy j2
sudo virsh undefine j2



#####################################################33
# vSRX01

#17.3R2
cp /mnt/images-repo/media-vsrx-vmdisk-17.3R2.10.qcow2 /var/lib/libvirt/images/vSRX01.qcow2


virt-install --name vSRX01 --memory 4096 --cpu SandyBridge,+vmx,-invtsc --vcpus=2 \
        --arch=x86_64 \
        --graphics vnc,listen=0.0.0.0 --noautoconsole \
        --disk path=/var/lib/libvirt/images/vSRX01.qcow2,size=16,device=disk,bus=ide,format=qcow2 \
        --os-type linux --os-variant rhel7 \
        --network=network:vmMgmt1,model=virtio \
        --network=network:dmz,model=virtio \
        --network=network:wan1101,model=virtio \
        --network=network:vmMgmt1,model=virtio \
        --network=network:vmMgmt1,model=virtio \
        --network=network:vmMgmt1,model=virtio \
        --network=network:vmMgmt1,model=virtio \
        --import


