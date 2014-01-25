apache2:                 # ID declaration
  pkg:                   # state declaration
    - installed          # function declaration
  service:
    - running
    - require:
      - pkg: apache2


