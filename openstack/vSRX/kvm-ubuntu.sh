virt-install --name u1 \
    --memory 1024 \
    --vcpus=1 \
    --graphics vnc,listen=0.0.0.0 --noautoconsole \
    --disk path=/var/lib/libvirt/images/u1.qcow2,size=16,device=disk,format=qcow2 \
    --os-type linux \
    --os-variant generic \
    --import

virt-install \
--name u1 \
--ram 1024 \
--disk path=/var/lib/libvirt/images/u1.qcow2,size=8 \
--vcpus 1 \
--os-type linux \
--os-variant generic \
--network network:wan1101,model=virtio \
--graphics none \
--console pty,target_type=serial \
--import
