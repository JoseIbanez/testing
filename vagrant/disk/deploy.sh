sudo apt-get install -y lvm2

fdisk -l /dev/sdc 
fdisk /dev/sdc << EOF
o
w
EOF


parted /dev/sdc mkpart primary ext4 1 50
pvcreate /dev/sdc1
vgcreate vg0 /dev/sdc1
lvcreate -L 5M -n lv1 vg0
mkfs.ext3 /dev/mapper/vg0-lv1
mount /dev/mapper/vg0-lv1 /mnt

fdisk -l /dev/sdc
df -h

##########
parted /dev/sdc resizepart 1 4GB
pvresize /dev/sdc1
lvextend -l +100%FREE /dev/mapper/vg0-lv1
resize2fs /dev/mapper/vg0-lv1

fdisk -l /dev/sdc
df -h


