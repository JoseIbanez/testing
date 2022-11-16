

virsh net-define ./net-nodes.xml
virsh net-start vlan-nodes
virsh net-autostart vlan-nodes

virsh net-list
virsh net-dumpxml vlan-nodes
ifconfig