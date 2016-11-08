function boot-hd {

param ($name)

$myVm=Get-VM -name $name

#Set boot order
echo "Set BootOrder"
$VMName = $myVM | get-view
$HDD1Key = ($VMName.Config.Hardware.Device | ?{$_.DeviceInfo.Label -eq "Hard Disk 1"}).Key
$bootHDD1 = New-Object -TypeName VMware.Vim.VirtualMachineBootOptionsBootableDiskDevice -Property @{"DeviceKey" = $HDD1Key}
$BootCD = New-Object -Type VMware.Vim.VirtualMachineBootOptionsBootableCdromDevice
 
$spec = New-Object VMware.Vim.VirtualMachineConfigSpec -Property @{"BootOptions" = New-Object VMware.Vim.VirtualMachineBootOptions -Property @{ BootOrder = $BootHDD1, $BootCD } }
$VMName.ReconfigVM_Task($spec)

}