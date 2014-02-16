switf:
  pkg.installed:
    - pkgs:
      - swift
      - swift-account 
      - swift-container 
      - swift-object 
      - xfsprogs

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



/srv/node/vdb1:
  mount.mounted:
    - device: /dev/vdb1
    - fstype: xfs
    - mkmnt: True
    - opts:
      - noatime
      - nodiratime
      - nobarrier
      - logbufs=8


