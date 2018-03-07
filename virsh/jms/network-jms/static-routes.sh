


auto eth0
iface eth0 inet static
      . . . 
      up route add -net 10.10.201.0 netmask 255.255.255.0 gw 10.10.20.1



route add -net 172.30.20.0/24 gw 10.11.1.1
route add -net 10.64.102.0/23 gw 10.11.1.1
