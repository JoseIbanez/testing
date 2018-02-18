
#main guide
http://brezular.com/2012/07/03/installing-olive-12-1r1-9-under-qemu/

#old freebsd images
http://mirrors.metapeer.com/FreeBSD-Archive/old-releases/i386/ISO-IMAGES/4.11/

#old ciphers
http://lucamattarozzi.blogspot.com.es/2016/07/debian8ubuntu-1604-with-openssh-7-re.html



virt-install \
--name o2 \
--ram 1024 \
--disk path=/var/lib/libvirt/images/o2.qcow2,size=16 \
--vcpus 1 \
--os-type generic \
--os-variant generic \
--network=network:mgmt,model=e1000 \
--graphics vnc,listen=0.0.0.0 --noautoconsole \
--console pty,target_type=serial \
--cdrom /mnt/images-repo/4.11-RELEASE-i386-miniinst.iso


sudo virsh dumpxml --security-info  o2 | grep graphics
sudo virsh update-device o2 ./vnc.xml 
sudo virsh dumpxml --security-info  o2 | grep graphics

virsh domiflist o2

    <interface type='network'>
      <source network='wan1101'/>
      <target dev='ge-000-j2'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
    </interface>



virsh attach-interface --domain o2 \
    --type network \
    --source wan1101 \
    --model e1000 \
    --config --live

    