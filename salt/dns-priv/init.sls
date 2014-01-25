bind9:
  pkg:
    - installed
  service:
    - running
    - watch:
      - file: /etc/bind/named.conf.local
      - file: /etc/bind/named.conf.options
    - require:
      - pkg: bind9

/etc/bind/named.conf.local:                            
  file:                                     
    - managed                              
    - source: salt://dns-priv/named.conf.local
    - user: root
    - group: bind
    - mode: 644
    - require:
      - pkg: bind9

/etc/bind/named.conf.options:
  file:
    - managed
    - source: salt://dns-priv/named.conf.options
    - user: root
    - group: bind
    - mode: 644   
    - require:
      - pkg: bind9

