hadoop:
  group.present:  
    - gid: 1010


hduser:
  user.present:
    - fullname: Hadoop User
    - shell: /bin/bash
    - home: /home/hduser
    - uid: 1010
    - gid: 1010
    - groups:
      - hadoop
    - require:
      - group: hadoop 
  ssh_auth:
    - present
    - user: hduser
    - source: salt://hadoop/hadoop.pub
    - require:
      - user: hduser


xfsprogs:
  pkg.installed


/home/ubuntu/java-install.sh:
  file:
    - managed
    - source: salt://hadoop/java-install.sh
    - user: root
    - group: root
    - mode: 755

/home/ubuntu/hadoop-install.sh:
  file:
    - managed
    - source: salt://hadoop/hadoop-install.sh
    - user: root
    - group: root
    - mode: 755

/home/ubuntu/hbase-install.sh:
  file:
    - managed
    - source: salt://hadoop/hbase-install.sh
    - user: root
    - group: root
    - mode: 755


/etc/sysctl.conf:
  file:
    - managed
    - source: salt://hadoop/sysctl.conf
    - user: root
    - group: root

/etc/profile:
  file:
    - managed
    - source: salt://hadoop/profile
    - user: root
    - group: root

/etc/hosts:
  file:
    - managed
    - source: salt://hadoop/hosts
    - user: root
    - group: root


/home/hduser/.bashrc:
  file:
    - managed
    - source: salt://hadoop/bashrc
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser



/usr/local/hadoop/etc/hadoop/yarn-site.xml:
  file:
    - managed
    - source: salt://hadoop/yarn-site.xml
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser

/usr/local/hadoop/etc/hadoop/core-site.xml:
  file:
    - managed
    - source: salt://hadoop/core-site.xml
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser

/usr/local/hadoop/etc/hadoop/mapred-site.xml:
  file:
    - managed
    - source: salt://hadoop/mapred-site.xml
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser

/usr/local/hadoop/etc/hadoop/hdfs-site.xml:
  file:
    - managed
    - source: salt://hadoop/hdfs-site.xml
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser

/usr/local/hadoop/etc/hadoop/hadoop-env.sh:
  file:
    - managed
    - source: salt://hadoop/hadoop-env.sh
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser

/usr/local/hadoop/etc/hadoop/slaves:
  file:
    - managed
    - source: salt://hadoop/slaves
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser




/usr/local/hbase/conf/hbase-site.xml:
  file:
    - managed
    - source: salt://hadoop/hbase-site.xml
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser

/usr/local/hbase/conf/hbase-env.sh:
  file:
    - managed
    - source: salt://hadoop/hbase-env.sh
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser


/usr/local/hbase/conf/backup-masters:  
  file:
    - managed
    - source: salt://hadoop/backup-masters  
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser                      


/usr/local/hbase/conf/regionservers:
  file:                                   
    - managed
    - source: salt://hadoop/regionservers
    - user: hduser
    - group: hadoop
    - require:
      - user: hduser





/mnt/hadoop/s1:
  file.directory:
    - user: hduser
    - group: hadoop
  mount.mounted:
    - device: /dev/vdb1
    - fstype: ext4
    - mkmnt: True
    - opts:
      - noatime
      - nodiratime
      - nobarrier
   

/mnt/hadoop/s2:
  file.directory:
    - user: hduser
    - group: hadoop
  mount.mounted:
    - device: /dev/vdc1
    - fstype: xfs
    - mkmnt: True
    - opts:
      - noatime
      - nodiratime
      - nobarrier
      - logbufs=8


/mnt/hadoop/s1/namenode:
  file.directory:
    - user: hduser
    - group: hadoop
    - require: 
       - file: /mnt/hadoop/s1

/mnt/hadoop/s1/datanode:
  file.directory:
    - user: hduser
    - group: hadoop
    - require: 
       - file: /mnt/hadoop/s1

/mnt/hadoop/s1/yarn-tmp:
  file.directory:
    - user: hduser
    - group: hadoop
    - require: 
       - file: /mnt/hadoop/s1

