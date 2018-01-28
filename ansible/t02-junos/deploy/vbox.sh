

set PATH=%PATH%;"C:\Program Files\Oracle\VirtualBox"

#windows
ova="C:/Users/jose.ibanez/Downloads/Juniper JunOS Olive12.1R1.9 Virtualbox image.ova"
name="JunOS-jc0201"
mgmtInt="VirtualBox Host-Only Ethernet Adapter"
pipePrefix="\\.\pipe\."


#Mac
ova="/Volumes/Data/Software/Juniper JunOS Olive12.1R1.9 Virtualbox image.ova"
mgmtInt="vboxnet0"
pipePrefix="/tmp/"


function create_ce {
    VBoxManage import "$ova" --vsys 0 --vmname $name

    VBoxManage modifyvm $name \
        --nic1 hostonly --hostonlyadapter1 $mgmtInt \
        --nic2 intnet --intnet2 "mpls-$site" \
        --nic3 intnet --intnet3 "lan-$site" \
        --uartmode1 server "$pipePrefix$name" \
        --audio none

    VBoxManage showvminfo $name
}


function create_pe {
    VBoxManage import "$ova" --vsys 0 --vmname $name

    VBoxManage modifyvm $name \
        --nic1 hostonly --hostonlyadapter1 $mgmtInt \
        --uartmode1 server "$pipePrefix$name" \
        --audio none

    VBoxManage showvminfo $name
}

name="jpe-1"
jpe1=$name
#create_pe
VBoxManage modifyvm $name \
    --nic8 intnet --intnet8 "core1" 


name="jpe-2"
jpe2=$name
#create_pe
VBoxManage modifyvm $name \
    --nic8 intnet --intnet8 "core1" 



site="0101"
name="jce-$site"
#create_ce
VBoxManage modifyvm $jpe1 \
    --nic2 intnet --intnet2 "mpls-$site" 


site="0102"
name="jce-$site"
#create_ce
VBoxManage modifyvm $jpe2 \
    --nic2 intnet --intnet2 "mpls-$site" 



site="0201"
name="jce-$site"
#create_ce
VBoxManage modifyvm $jpe1 \
    --nic3 intnet --intnet3 "mpls-$site" 

site="0202"
name="jce-$site"
#create_ce
VBoxManage modifyvm $jpe2 \
    --nic3 intnet -intnet3 "mpls-$site" 




VBoxManage modifyvm $jpe1 \
    --nic5 intnet --intnet5 "unused"
VBoxManage modifyvm $jpe1 \
    --nic6 intnet --intnet6 "unused"
VBoxManage modifyvm $jpe1 \
    --nic7 intnet --intnet7 "unused"
     

VBoxManage modifyvm $jpe2 \
    --nic5 intnet --intnet5 "unused"
VBoxManage modifyvm $jpe2 \
    --nic6 intnet --intnet6 "unused"
VBoxManage modifyvm $jpe2 \
    --nic7 intnet --intnet7 "unused"
     


