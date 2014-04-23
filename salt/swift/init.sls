ubuntu-cloud-keyring:
  pkg.installed

ubuntu-cloud:
  pkgrepo.managed:
    - humanname: Ubuntu Cloud Havana
    - name: deb http://ubuntu-cloud.archive.canonical.com/ubuntu precise-updates/havana main
    - file: /etc/apt/sources.list.d/cloudarchive-havana.list
    - keyserver: ubuntu-cloud.archive.canonical.com
    - required:
      - pkg: ubuntu-cloud-keyring
    - require_in:
      - pkg: swift

swift:
  pkg.installed:
    - pkgs:
      - swift
      - swift-account 
      - swift-container 
      - swift-object 


xfsprogs:
  pkg.installed



rsync:
  service:
    - running
    - watch:
      - file: /etc/default/rsync
      - file: /etc/rsyncd.conf

/etc/rsyncd.conf:
  file:
    - managed
    - source: salt://swift/rsyncd.conf

/etc/default/rsync:
  file:
    - managed
    - source: salt://swift/rsyncd-default


/home/fibratel/.ssh/swf_id_rsa:
  file:
    - managed
    - source: salt://swift/swf_id_rsa
    - user: fibratel
    - group: fibratel
    - mode: 600

/home/fibratel/swift/ring.sh:
  file:
    - managed
    - source: salt://swift/ring.sh
    - user: fibratel
    - group: fibratel
    - mode: 755


/etc/swift/swift.conf:
  file:
    - managed
    - source: salt://swift/swift.conf
    - user: swift
    - group: swift

/etc/swift/account-server.conf:
  file:
    - managed
    - source: salt://swift/account-server.conf

/etc/swift/container-server.conf:
  file:
    - managed
    - source: salt://swift/container-server.conf

/etc/swift/object-server.conf:
  file:
    - managed
    - source: salt://swift/object-server.conf


/etc/swift:
  file.directory:
    - user: swift
    - group: swift
    - recurse:
      - user
      - group
    
/var/run/swift:
  file.directory:
    - user: swift
    - group: swift

/var/cache/swift:
  file.directory:
    - user: swift
    - group: swift



/srv/node/sdb1:
  mount.mounted:
    - device: /dev/sdb1
    - fstype: xfs
    - mkmnt: True
    - opts:
      - noatime
      - nodiratime
      - nobarrier
      - logbufs=8

/srv/node/sdc1:
  mount.mounted:
    - device: /dev/sdc1
    - fstype: xfs
    - mkmnt: True
    - opts:
      - noatime
      - nodiratime
      - nobarrier
      - logbufs=8


