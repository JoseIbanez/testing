https://www.youtube.com/watch?v=pPO75mWN1xw

1) Download CUCM iso file from cisco.com:
UCSInstall_UCOS_10.5.1.10000-7.sgn.iso

2) Create the directory for mounting the iso file:
sudo mkdir /mnt/iso

3) Mount the iso file:
sudo mount -o loop UCSInstall_UCOS_10.5.1.10000-7.sgn.iso /mnt/iso/

4) Create the directory for editing files:
mkdir /tmp/CUCM

5) Copy the files to temp directory:
rsync -a /mnt/iso/ /tmp/CUCM/

6) Enable KVM support by renaming the file:
cd /tmp/CUCM_custom/Cisco/hssi/server_imple­mentation/KVM/QEMU/shared/bin
mv api_implementation.sh.proposed api_implementation.sh

7) Edit hasHwSnmpMonitoring function in Cisco/base_scripts/ihardware.sh:
vi /tmp/CUCM/Cisco/base_scripts/ihardware.s­h

The function should look like:
function hasHwSnmpMonitoring()
{ return 1
}

8) Create bootable iso file:
mkisofs -o /tmp/Bootable_UCSInstall_UCOS_10.5.1.100­00-7.sgn.iso -b
isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4
-boot-info-table -J -R .

