virsh net-list

virsh net-destroy wan1101
virsh net-destroy wan1102

virsh net-undefine wan1101
virsh net-undefine wan1102

###############
#http://wiki.flav.com/wiki/Open_vSwitch_Tutorial

ovs-vsctl add-br br0
ovs-vsctl add-port br0 enp6s0

ovs-vsctl add-port br0 tap0 tag=9

ifconfig br0 up

ip tuntap add mode tap tap0
ifconfig tap0 up

ip tuntap add mode tap wan1101
ip tuntap add mode tap wan1102
ifconfig wan1101 up
ifconfig wan1102 up

ovs-vsctl add-port br0 wan1101 tag=1101
ovs-vsctl add-port br0 wan1102 tag=1102

ovs-vsctl show
ovs-vsctl del-br br0



#https://blog.scottlowe.org/2012/11/07/using-vlans-with-ovs-and-libvirt/



#https://www.opencloudblog.com/?p=177

ovs-vsctl del-br ovs0

ovs-vsctl show



ovs-vsctl add-br ovs0
ovs-vsctl add-port ovs0 enp6s0
ovs-vsctl del-port ovs0 enp6s0

ifconfig ovs0 up
ovs-vsctl show


virsh net-define ./wan1101.xml
virsh net-start wan1101
virsh net-autostart wan1101

virsh domiflist u2
ovs-vsctl show

virsh domiflist j2
ovs-vsctl show

