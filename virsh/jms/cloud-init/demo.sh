

mkdir /tmp/u3
rm -rf /tmp/u3/*
cp ./u3/* /tmp/u3/
genisoimage -o /tmp/u3/config.iso -V cidata -r -J /tmp/u3/


sudo cp /mnt/images-repo/xenial-server-cloudimg-amd64-disk1.img /var/lib/libvirt/images/u3.qcow2

virt-install \
--name u3 \
--ram 1024 \
--disk path=/var/lib/libvirt/images/u3.qcow2,size=8 \
--vcpus 1 \
--os-type linux \
--os-variant generic \
--network network=mgmt \
--network network:wan1101,model=virtio \
--network network:wan1102,model=virtio \
--graphics none \
--console pty,target_type=serial \
--disk path=/tmp/u3/config.iso,device=cdrom \
--import

virsh domiflist u3

