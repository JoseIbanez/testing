@L show_run
show run

@L interfaces
show interfaces summary

@L ntp
show ntp associations

@L create_vlans
conf t
vlan 1600
 name Cust16_Inside
vlan 1601
 name Cust16_InterDC
vlan 1602
 name Cust16_Management
vlan 1603
 name Cust16_OutSide
exit
end

@L upInterface
conf t
int e0/0
no shut
exit
end
