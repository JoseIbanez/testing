admin:
  group.present:  
    - gid: 1010

super:
  group.present:
    - gid: 1011

  
/etc/sudoers.d/super:
  file.managed:
    - source: salt://users/sudoers
    - user: root
    - group: root
    - mode: 440    


ibanez:
  user.present:
    - fullname: Jose Ibanez
    - shell: /bin/bash
    - home: /home/ibanez
    - uid: 1213
    - gid: 1010
    - groups:
      - admin
      - super
    - require:
      - group: admin
      - group: super 
  ssh_auth:
    - present
    - user: ibanez
    - source: salt://users/ibanez.pub
    - require:
      - user: ibanez

joseiba:
  user.present:
    - fullname: Jose Ibanez
    - shell: /bin/bash
    - home: /home/joseiba
    - uid: 1003
    - gid: 1010
    - groups:
      - admin
      - super
    - require:
      - group: admin
      - group: super 
  ssh_auth:
    - present
    - user: joseiba
    - source: salt://users/joseiba.pub
    - require:
      - user: joseiba

