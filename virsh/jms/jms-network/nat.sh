https://albertomolina.wordpress.com/2009/01/09/nat-con-iptables/

iptables -t nat -L -n


iptables -t nat -A POSTROUTING -s 10.10.2.0/24 -o eth0 -j SNAT --to 85.112.1.104


:85.112.1.104
