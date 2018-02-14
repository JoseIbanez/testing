virt-install --name u1 \
    --memory 1024 \
    --vcpus=1 \
    --graphics vnc,listen=0.0.0.0 --noautoconsole \
    --disk path=/var/lib/libvirt/images/u1.qcow2,size=16,device=disk,format=qcow2 \
    --os-type linux \
    --os-variant generic \
    --import

guestmount -a /var/lib/libvirt/images/u1.qcow2 -m /dev/sda1 /media

virt-install \
--name u2 \
--ram 1024 \
--disk path=/var/lib/libvirt/images/u2.qcow2,size=8 \
--vcpus 1 \
--os-type linux \
--os-variant generic \
--network network=mgmt \
--network network:wan1101,model=virtio \
--graphics none \
--console pty,target_type=serial \
--import


https://www.cyberciti.biz/faq/how-to-add-ssh-public-key-to-qcow2-linux-cloud-images-using-virt-sysprep/

