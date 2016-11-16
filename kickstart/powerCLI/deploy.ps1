
$name="UKXSW1SV24"
$h="ukxsw1ex03013.swi.cww-hcs.com"
$storage="HCS-SWI-VMAX-LUN-11"
$cores=4
$ram=8
$disk=40
$rMHz=0

$name="UKXSW1SV25"
$h="ukxsw1ex03013.swi.cww-hcs.com"
$storage="HCS-SWI-VMAX-LUN-12"
$cores=4
$ram=8
$disk=40
$rMHz=0



function deploy-tropo {


param ($name,$h,$storage,$cores,$ram,$disk,$rMHz)


#Clone from template
echo "Clone Template"
$myVm=New-VM -name $name   -Datastore $storage  -Template KubernetesTemplate -location "Cisco Support TROPO"  -vmhost $h 
#$myVm=New-VM -name $name   -Datastore $storage  -Template KubernetesTemplate -location Tropo  -vmhost $h 
#-resourcepool $h

#Change Cores,RAM,Disk,...
$spec=New-Object –Type VMware.Vim.VirtualMAchineConfigSpec –Property @{"NumCoresPerSocket" = $cores}
($myVM).ExtensionData.ReconfigVM_Task($spec)

echo "Set #Cores, RAM, Disk"
$myVm | Set-vm -MemoryGB $ram -NumCpu $cores -confirm:$false
$myVM | Get-VMResourceConfiguration | Set-VMResourceConfiguration -CpuReservationMhz $rMHz
#$myVM | Get-HardDisk | where {$_.Name -eq "Hard disk 1"} | Set-HardDisk -CapacityGB $disk -confirm:$false


#Connect DVD
echo "Connect DVD"
$cd=Get-CDDrive -VM $name
#Set-CDDrive -CD $cd -IsoPath "[pub] iso/RedHat/Tropo_KS-x86_64.iso" -StartConnected $true -confirm:$false
Set-CDDrive -CD $cd -IsoPath "[HCS-SWI-VMAX-LUN-27] TROPO-DWP/rhel-server-7.2-x86_64-dvd-ks.iso" -StartConnected $true -confirm:$false


#Connect Floppy
echo "Connect Floppy"
$fp=Get-FloppyDrive -VM  $name
$fpPath="[HCS-SWI-VMAX-LUN-27] TROPO-DWP/"+$name+".img"
Set-FloppyDrive -Floppy $fp -FloppyImagePath $fpPath -StartConnected $true  -confirm:$false


#Set boot order
echo "Set BootOrder"
$VMName = $myVM | get-view
$HDD1Key = ($VMName.Config.Hardware.Device | ?{$_.DeviceInfo.Label -eq "Hard Disk 1"}).Key
$bootHDD1 = New-Object -TypeName VMware.Vim.VirtualMachineBootOptionsBootableDiskDevice -Property @{"DeviceKey" = $HDD1Key}
$BootCD = New-Object -Type VMware.Vim.VirtualMachineBootOptionsBootableCdromDevice
 
$spec = New-Object VMware.Vim.VirtualMachineConfigSpec -Property @{"BootOptions" = New-Object VMware.Vim.VirtualMachineBootOptions -Property @{ BootOrder = $BootCD, $BootHDD1 } }
$VMName.ReconfigVM_Task($spec)


#Start VM
echo "Start VM"
$myVM | start-vm
}
