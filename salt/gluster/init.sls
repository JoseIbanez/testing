semiosis:
  pkgrepo.managed:
    - humanname: Semiosis PPA (Gluster Official Repo)
    - name: deb http://ppa.launchpad.net/semiosis/ubuntu-glusterfs-3.4/ubuntu/ precise main
    - dist: precise
    - file: /etc/apt/sources.list.d/semiosis.list
    - keyid: 774BAC4D
    - keyserver: keyserver.ubuntu.com
    - require_in:
      - pkg: 

  pkg.lastest:
    - name: glusterfs-server
    - refresh: True

