


auto eth0
iface eth0 inet static
      . . . 
      up route add -net 10.10.201.0 netmask 255.255.255.0 gw 10.10.20.1
