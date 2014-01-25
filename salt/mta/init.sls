
postfix:
  pkg:
    - installed
  service:
    - running
    - watch:
      - file: /etc/mta.conf
    - require:
      - pkg: postfix


/etc/mta.conf:                              # ID declaration
  file:                                     # state declaration
    - managed                               # function
    - source: salt://mta/mta.conf        # function arg

