#!/bin/sh

#
# https://www.howtoforge.com/puppet-ubuntu-14.04
#

puppet cert list --all

cp -av puppet/modules/*   /etc/puppet/modules/
cp -av puppet/manifests/* /etc/puppet/manifests/


service puppet restart

puppet cert sign u10
puppet cert sign --all

for i in `seq 30 39`;
do
  lxc exec u$i -- /usr/bin/puppet agent --enable
done
tail -f /var/log/syslog

for i in `seq 30 39`;
do
  lxc exec u$i -- /usr/bin/puppet agent -t
done
