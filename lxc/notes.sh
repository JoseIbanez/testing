# docker + lxd

ref: https://discuss.linuxcontainers.org/t/lxd-and-docker-firewall-redux-how-to-deal-with-forward-policy-set-to-drop/9953/3


sudo iptables -I DOCKER-USER  -j ACCEPT


