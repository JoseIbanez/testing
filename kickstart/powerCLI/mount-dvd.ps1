



$name="UKXSW1SV12"

dvd-tropo -name 

function dvd-tropo {
param ($name)


$pass="VFhcs123!"

Invoke-VMScript -ScriptText  "umount /media"        -VM $name -GuestUser root -GuestPassword $pass
Invoke-VMScript -ScriptText  "eject /dev/cdrom"     -VM $name -GuestUser root -GuestPassword $pass



#Connect DVD

echo "Connect DVD"
$cd=Get-CDDrive -VM $name
Set-CDDrive -CD $cd -IsoPath "[HCS-SWI-VMAX-LUN-27] TROPO-DWP/tropo_dark_15.5.0.iso" -StartConnected $true  -Connected $true -confirm:$false


Invoke-VMScript -ScriptText "mount /dev/cdrom /media"     -VM $name -GuestUser root -GuestPassword $pass
Invoke-VMScript -ScriptText "mount"     -VM $name -GuestUser root -GuestPassword $pass
Invoke-VMScript -ScriptText "ls -l /media/"     -VM $name -GuestUser root -GuestPassword $pass

}




$net=Get-NetworkAdapter -VM $name
Set-NetworkAdapter -NetworkAdapter $net -Connected $true -StartConnected $true
