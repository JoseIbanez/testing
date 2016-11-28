@L po1
conf t
!
default int e0/0
default int po1
!
int po1
description IntraDC
switchport
switchport trunk encapsulation dot1q
switchport mode trunk
!
int e0/0
description IntraDC
switchport
switchport trunk encapsulation dot1q
switchport mode trunk
channel-group 1 mode active
duplex full
!
int po1
switchport trunk allowed vlan 1000
!
int e0/0
switchport trunk allowed vlan 1000
!
!
!
!
default int e1/0
default int po11
!
int po11
description InterDC
switchport
switchport trunk encapsulation dot1q
switchport mode trunk
!
int e1/0
description InterDC
switchport
switchport trunk encapsulation dot1q
switchport mode trunk
channel-group 11 mode active
duplex full
!
int po11
switchport trunk allowed vlan 1001
!
int e1/0
switchport trunk allowed vlan 1001
!
end
wr
@L sh_run
show run
@L sh_po
show etherchannel summary
exit
