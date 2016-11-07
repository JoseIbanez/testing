#!/bin/sh

cat > /etc/yum.repos.d/rhel7dvd.repo << EOF
[InstallMedia]
name=Red Hat Enterprise Linux 7.2
mediaid=1446216863.790260
metadata_expire=-1
gpgcheck=1
cost=500
enabled=1
baseurl=file:///media/
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
EOF

chmod 644 /etc/yum.repos.d/rhel7dvd.repo

yum clean all
subscription-manager clean
yum list --noplugin
