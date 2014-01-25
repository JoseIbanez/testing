ntp:
  pkg:
    - installed
  service:
    - running
    - watch:
      - file: /etc/ntp.conf
    - require:
      - pkg: ntp


/etc/ntp.conf:                            
  file:                                     
    - managed                              
    - source: salt://ntp/ntp.conf
