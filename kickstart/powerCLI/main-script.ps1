deploy-tropo -name "tropo.01" -h "EX11" -storage "CDHP"  -cores 2 -ram 2 -disk 10 -rMHz 100
deploy-tropo -name "tropo.02" -h "EX12" -storage "CDWD"  -cores 4 -ram 4 -disk 40 -rMHz 100
deploy-tropo -name "tropo.03" -h "EX31" -storage "CDWD"  -cores 1 -ram 1 -disk 20 -rMHz 100
deploy-tropo -name "tropo.04" -h "EX32" -storage "CDHP"  -cores 1 -ram 1 -disk 10 -rMHz 100
deploy-tropo -name "tropo.05" -h "EX11" -storage "CDHP"  -cores 2 -ram 2 -disk 10 -rMHz 100
deploy-tropo -name "tropo.06" -h "EX12" -storage "CDWD"  -cores 4 -ram 4 -disk 40 -rMHz 100
deploy-tropo -name "tropo.07" -h "EX31" -storage "CDWD"  -cores 1 -ram 1 -disk 20 -rMHz 100
deploy-tropo -name "tropo.08" -h "EX32" -storage "CDHP"  -cores 1 -ram 1 -disk 10 -rMHz 100

deploy-tropo -name "UKXSW1SV26" -h "ukxsw1ex03014.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-13"  -cores 4 -ram 8 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV27" -h "ukxsw1ex03014.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-14"  -cores 16 -ram 72 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV28" -h "ukxsw1ex03013.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-15"  -cores 16 -ram 72 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV29" -h "ukxsw1ex03014.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-16"  -cores 16 -ram 72 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV30" -h "ukxsw1ex03015.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-17"  -cores 16 -ram 72 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV31" -h "ukxsw1ex03015.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-18"  -cores 20 -ram 80 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV34" -h "ukxsw1ex03013.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-19"  -cores 4 -ram 16 -disk40 -rMHz 0



stop-vm -vm "UKXSW1SV24" -confirm:$false
stop-vm -vm "UKXSW1SV25" -confirm:$false
stop-vm -vm "tropo.03" -confirm:$false
stop-vm -vm "tropo.04" -confirm:$false
stop-vm -vm "tropo.05" -confirm:$false
stop-vm -vm "tropo.06" -confirm:$false
stop-vm -vm "tropo.07" -confirm:$false
stop-vm -vm "tropo.08" -confirm:$false



boot-hd -name "UKXSW1SV24"
boot-hd -name "UKXSW1SV25"
boot-hd -name "tropo.03"
boot-hd -name "tropo.04"
boot-hd -name "tropo.05"
boot-hd -name "tropo.06"
boot-hd -name "tropo.07"
boot-hd -name "tropo.08"




start-vm -vm "UKXSW1SV24" 
start-vm -vm "UKXSW1SV25" 
start-vm -vm "tropo.03" 
start-vm -vm "tropo.04" 
start-vm -vm "tropo.05" 
start-vm -vm "tropo.06" 
start-vm -vm "tropo.07" 
start-vm -vm "tropo.08" 





Invoke-VMScript -ScriptText "sed -i 's/BOOTPROTO=.*/BOOTPROTO=none/g' /etc/sysconfig/network-scripts/ifcfg-ens32 " -VM "UKXSW1SV17" -GuestUser root -GuestPassword VFhcs123!

Invoke-VMScript -ScriptText "sed -i 's/ONBOOT=.*/BOOTPROTO=yes/g' /etc/sysconfig/network-scripts/ifcfg-ens32"      -VM "UKXSW1SV17" -GuestUser root -GuestPassword VFhcs123!

Invoke-VMScript -ScriptText "ifup ens32; ifconfig"                                                                 -VM "UKXSW1SV17" -GuestUser root -GuestPassword VFhcs123!



Invoke-VMScript -ScriptText "df" -VM "UKXSW1SV24" -GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.03"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.04"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.05"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.06"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.07"-GuestUser root -GuestPassword passw0rd
Invoke-VMScript -ScriptText "df" -VM "tropo.08"-GuestUser root -GuestPassword passw0rd




Invoke-VMScript -ScriptText "sed -i 's/BOOTPROTO=.*/BOOTPROTO=none/g' /etc/sysconfig/network-scripts/ifcfg-ens32 " -VM "UKXSW1SV20" -GuestUser root -GuestPassword VFhcs123!
Invoke-VMScript -ScriptText "sed -i 's/ONBOOT=.*/BOOTPROTO=yes/g' /etc/sysconfig/network-scripts/ifcfg-ens32"      -VM "UKXSW1SV20" -GuestUser root -GuestPassword VFhcs123!
Invoke-VMScript -ScriptText "ifup ens32; ifconfig ens32"                                                           -VM "UKXSW1SV20" -GuestUser root -GuestPassword VFhcs123!

Invoke-VMScript -ScriptText "sed -i 's/BOOTPROTO=.*/BOOTPROTO=none/g' /etc/sysconfig/network-scripts/ifcfg-eth0 " -VM "UKXSW1SV21" -GuestUser root -GuestPassword VFhcs123!
Invoke-VMScript -ScriptText "sed -i 's/ONBOOT=.*/BOOTPROTO=yes/g' /etc/sysconfig/network-scripts/ifcfg-eth0"      -VM "UKXSW1SV21" -GuestUser root -GuestPassword VFhcs123!
Invoke-VMScript -ScriptText "ifup eth0; ifconfig eth0"                                                          -VM "UKXSW1SV21" -GuestUser root -GuestPassword VFhcs123!


$VMname="UKXLS2SV21"
$pass="VFhcs123!"

Invoke-VMScript -ScriptText "cat /proc/net/dev"     -VM $VMname -GuestUser root -GuestPassword $pass
Invoke-VMScript -ScriptText "cat /etc/sysconfig/network-scripts/ifcfg-eth0" -VM $VMname -GuestUser root -GuestPassword $pass
Invoke-VMScript -ScriptText "cat /etc/udev/rules.d/70-persistent-net.rules"     -VM $VMname -GuestUser root -GuestPassword $pass


Invoke-VMScript -ScriptText "rm /etc/udev/rules.d/70-persistent-net.rules"     -VM $VMname -GuestUser root -GuestPassword $pass
Invoke-VMScript -ScriptText "sed -i 's/BOOTPROTO=.*/BOOTPROTO=none/g' /etc/sysconfig/network-scripts/ifcfg-eth0 " -VM $VMname -GuestUser root -GuestPassword $pass
Invoke-VMScript -ScriptText "sed -i 's/ONBOOT=.*/ONBOOT=yes/g' /etc/sysconfig/network-scripts/ifcfg-eth0"      -VM $VMname -GuestUser root -GuestPassword $pass
Invoke-VMScript -ScriptText "sed -i 's/HWADDR=.*//g' /etc/sysconfig/network-scripts/ifcfg-eth0"      -VM $VMname -GuestUser root -GuestPassword $pass

Invoke-VMScript -ScriptText "init 6"    -VM $VMname -GuestUser root -GuestPassword $pass

Invoke-VMScript -ScriptText "ifconfig"                                                          -VM $VMname -GuestUser root -GuestPassword $pass
Invoke-VMScript -ScriptText "ifup eth0; ifconfig eth0"                                                          -VM $VMname -GuestUser root -GuestPassword $pass




$name="UKXSW1SV24"
$floppy = Get-FloppyDrive -VM $name
Remove-FloppyDrive -Floppy $floppy



deploy-tropo -name "UKXSW1SV26" -h "ukxsw1ex03014.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-13"  -cores 4 -ram 8 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV27" -h "ukxsw1ex03014.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-14"  -cores 16 -ram 72 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV28" -h "ukxsw1ex03013.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-15"  -cores 16 -ram 72 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV29" -h "ukxsw1ex03014.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-16"  -cores 16 -ram 72 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV30" -h "ukxsw1ex03015.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-17"  -cores 16 -ram 72 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV31" -h "ukxsw1ex03015.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-18"  -cores 20 -ram 80 -disk40 -rMHz 0
deploy-tropo -name "UKXSW1SV34" -h "ukxsw1ex03013.swi.cww-hcs.com" -storage "HCS-SWI-VMAX-LUN-19"  -cores 4 -ram 16 -disk40 -rMHz 0


stop-vm -vm "UKXSW1SV24" -confirm:$false
stop-vm -vm "UKXSW1SV25" -confirm:$false
stop-vm -vm "UKXSW1SV26" -confirm:$false
stop-vm -vm "UKXSW1SV27" -confirm:$false
stop-vm -vm "UKXSW1SV28" -confirm:$false
stop-vm -vm "UKXSW1SV29" -confirm:$false
stop-vm -vm "UKXSW1SV30" -confirm:$false
stop-vm -vm "UKXSW1SV31" -confirm:$false
stop-vm -vm "UKXSW1SV34" -confirm:$false

boot-hd -name "UKXSW1SV24"
boot-hd -name "UKXSW1SV25"
boot-hd -name "UKXSW1SV26"
boot-hd -name "UKXSW1SV27"
boot-hd -name "UKXSW1SV28"
boot-hd -name "UKXSW1SV29"
boot-hd -name "UKXSW1SV30"
boot-hd -name "UKXSW1SV31"
boot-hd -name "UKXSW1SV34"




start-vm -vm "UKXSW1SV24" 
start-vm -vm "UKXSW1SV25" 
start-vm -vm "UKXSW1SV26" 
start-vm -vm "UKXSW1SV27" 
start-vm -vm "UKXSW1SV28"
start-vm -vm "UKXSW1SV29"
start-vm -vm "UKXSW1SV30"
start-vm -vm "UKXSW1SV31"
start-vm -vm "UKXSW1SV34"

no-floppy -name "UKXSW1SV24" 
no-floppy -name "UKXSW1SV25" 
no-floppy -name "UKXSW1SV26" 
no-floppy -name "UKXSW1SV27" 
no-floppy -name "UKXSW1SV28"
no-floppy -name "UKXSW1SV29"
no-floppy -name "UKXSW1SV30"
no-floppy -name "UKXSW1SV31"
no-floppy -name "UKXSW1SV34"

$name="UKXSW1SV24"

function add-HD {
param ($name)
$vm = Get-VM $name
$vm | New-HardDisk -CapacityGB 80 -Persistence persistent
}

add-HD -name "UKXSW1SV24" 
add-HD -name "UKXSW1SV25" 
add-HD -name "UKXSW1SV26" 
add-HD -name "UKXSW1SV27" 
add-HD -name "UKXSW1SV28"
add-HD -name "UKXSW1SV29"
add-HD -name "UKXSW1SV30"
add-HD -name "UKXSW1SV31"

