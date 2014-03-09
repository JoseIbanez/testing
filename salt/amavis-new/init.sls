amavis-pkgs:
  pkg.installed:
    - pkgs:
       - postfix
       - amavisd-new
       - spamassassin
       - spamc
       - dnsutils 
       - patch 
       - flex 
       - bison
       - gdb
       - arj
       - unrar
       - nomarch
       - lzop
       - cabextract
       - libimage-info-perl
       - libnet-cidr-lite-perl
       - libmail-dkim-perl

postfix:
  service:
    - running
    - watch:
      - file: /etc/postfix/main.cf
      - file: /etc/postfix/master.cf
    - require:
      - pkg: amavis-pkgs


amavis:                            
  service:                                     
    - running
    - require:
      - pkg: amavis-pkgs
    - watch:
      - file: /etc/amavis/conf.d/50-user
   

spamassassin:
  service:
    - running
    - require:
      - pkg: amavis-pkgs

###

/etc/postfix/main.cf:
  file: 
    - managed                              
    - source: salt://amavis-new/postfix/main.cf
    - template: jinja


/etc/postfix/master.cf:
  file:
    - managed
    - source: salt://amavis-new/postfix/master.cf 

###

/etc/postfix/virtual:
  file:
    - managed
    - source: salt://amavis-new/postfix/virtual

/etc/postfix/transport:
  file:
    - managed
    - source: salt://amavis-new/postfix/transport

/etc/postfix/recipients:
  file:
    - managed
    - source: salt://amavis-new/postfix/recipients

/etc/postfix/sender_canonical:
  file:
    - managed
    - source: salt://amavis-new/postfix/sender_canonical

###

run-virtual:
  cmd.wait:
    - name: /usr/sbin/postmap /etc/postfix/virtual
    - cwd: /
    - watch:
      - file: /etc/postfix/virtual

run-transport:
  cmd.wait:
    - name: /usr/sbin/postmap /etc/postfix/transport
    - cwd: /
    - watch:
      - file: /etc/postfix/transport

run-sender:
  cmd.wait:
    - name: /usr/sbin/postmap /etc/postfix/sender_canonical
    - cwd: /
    - watch:
      - file: /etc/postfix/sender_canonical

run-recipients:
  cmd.wait:
    - name: /usr/sbin/postmap /etc/postfix/recipients
    - cwd: /
    - watch:
      - file: /etc/postfix/recipients

###

/etc/spamassasing/local.cf:
  file:
    - managed
    - source: salt://amavis-new/spamassasing/local.cf

###

/etc/amavis/conf.d/50-user:
  file:
    - managed
    - source: salt://amavis-new/amavis-new/50-user
    - template: jinja
   

/etc/amavis/conf.d/15-content_filter_mode:
  file:
    - managed
    - source: salt://amavis-new/amavis-new/15-content_filter_mode


