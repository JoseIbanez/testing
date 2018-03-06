https://albertomolina.wordpress.com/2009/01/09/nat-con-iptables/

iptables -t nat -L -n -v


iptables -t nat -D POSTROUTING -s 10.10.2.0/24   -o em1 -j SNAT --to 85.112.1.104


iptables -t nat -A POSTROUTING -s 10.10.5.0/24   -o em1 -j SNAT --to 85.112.1.104
iptables -t nat -A POSTROUTING -s 10.10.201.0/24 -o em1 -j SNAT --to 85.112.1.104
iptables -t nat -A POSTROUTING -s 10.10.202.0/24 -o em1 -j SNAT --to 85.112.1.104



# https://askubuntu.com/questions/119393/how-to-save-rules-of-the-iptables

iptables -t nat -L -n -v

sudo netfilter-persistent save
sudo netfilter-persistent reload

