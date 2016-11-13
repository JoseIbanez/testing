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

