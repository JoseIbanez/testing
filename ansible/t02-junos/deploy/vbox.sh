

set PATH=%PATH%;"C:\Program Files\Oracle\VirtualBox"

ova="C:/Users/jose.ibanez/Downloads/Juniper JunOS Olive12.1R1.9 Virtualbox image.ova"
name="JunOS-jc0201"

vboxmanage import "$ova" --vsys 0 --vmname $name

VBoxManage modifyvm $name \
    --nic1 hostonly --hostonlyadapter1 "VirtualBox Host-Only Ethernet Adapter" \
    --nic2 intnet --intnet2 mpls-c0201 \
    --nic3 intnet --intnet3 lan-c0201 \

VBoxManage infovm $name


