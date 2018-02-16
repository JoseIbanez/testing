
https://gist.github.com/umardx/a31bf6a13600a55c0d07d4ca33133834


yum -y install wget openssl-devel gcc make python-devel openssl-devel kernel-devel graphviz kernel-debug-devel autoconf automake rpm-build redhat-rpm-config libtool python-twisted-core python-zope-interface PyQt4 desktop-file-utils libcap-ng-devel groff checkpolicy selinux-policy-devel

  538  yum -y install wget openssl-devel gcc make python-devel openssl-devel kernel-devel graphviz kernel-debug-devel autoconf automake rpm-build redhat-rpm-config libtool python-twisted-core python-zope-interface PyQt4 desktop-file-utils libcap-ng-devel groff checkpolicy selinux-policy-devel
  539  adduser ovs
  540  su - ovs

    1  mkdir -p ~/rpmbuild/SOURCES
    2  wget http://openvswitch.org/releases/openvswitch-2.5.2.tar.gz
    3  cp openvswitch-2.5.2.tar.gz ~/rpmbuild/SOURCES/
    4  tar xfz openvswitch-2.5.2.tar.gz
    5  rpmbuild -bb --nocheck openvswitch-2.5.2/rhel/openvswitch-fedora.spec
    6  exit


  541  yum localinstall /home/ovs/rpmbuild/RPMS/x86_64/openvswitch-2.5.2-1.el7.centos.x86_64.rpm -y
  542  systemctl start openvswitch.service
  543  systemctl is-active openvswitch
  544  systemctl enable openvswitch
  545  ovs-vsctl -V