yum groupinstall -y 'Development Tools'
yum install -y net-tools

cd /tmp
tar -zxvf VMwareTools-*.tar.gz
cd vmware-tools-distrib
./vmware-install.pl -d default
