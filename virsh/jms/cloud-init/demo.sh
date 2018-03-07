

mkdir /tmp/u1
rm -rf /tmp/u1/*
cp ./u1/* /tmp/u1/
genisoimage -o /tmp/u1/config.iso -V cidata -r -J /tmp/u1/


sudo cp /mnt/images-repo/xenial-server-cloudimg-amd64-disk1.img /var/lib/libvirt/images/u1.qcow2

virt-install \
--name u1 \
--ram 1024 \
--disk path=/var/lib/libvirt/images/u1.qcow2,size=8 \
--vcpus 1 \
--os-type linux \
--os-variant generic \
--network network=vmMgmt1,model=virtio \
--network network:dmz,model=virtio \
--network network:wan1101,model=virtio \
--graphics none \
--console pty,target_type=serial \
--disk path=/home/ubuntu/u1/config.iso,device=cdrom \
--import

virsh domiflist u3

virsh destroy u1
virsh undefine u1


virt-install \
--name u1 \
--ram 1024 \
--disk path=/var/lib/libvirt/images/u1.qcow2,size=8 \
--vcpus 1 \
--os-type linux \
--os-variant generic \
--network network=vmMgmt \
--graphics none \
--console pty,target_type=serial \
--disk path=/home/ubuntu/u1/config.iso,device=cdrom \
--import

--disk path=/home/ubuntu/u1/config.iso,device=cdrom \


virsh domiflist u3


ip addr add 10.11.1.3 dev ens4
