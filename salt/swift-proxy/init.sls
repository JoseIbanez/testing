swift-proxy:
  pkg:
    - installed
  service:
    - running
    - watch:
      - file: /etc/swift/swift.conf
      - file: /etc/swift/proxy-server.conf  
    - require:
      - pkg: swift-proxy

memcached:
  pkg:
    - installed
  service:
    - running
    - watch:
      - file: /etc/memcached.conf
    - require:
      - pkg: memcached


/etc/memcached.conf:
  file:
    - managed
    - source: salt://swift-proxy/memcached.conf
    - user: root
    - group: root
    - mode: 640
    - require:
      - pkg: memcached
    - template: jinja
    - context:
        proxy_ip: {{ salt['network.interfaces']()['eth0']['inet'][0]['address'] }}
        storage_ip: {{ salt['network.ip_addrs']('eth0')[0] }}



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
    

/etc/swift/swift.conf:
  file:
    - managed
    - source: salt://swift/swift.conf
    - user: swift
    - group: swift

/etc/swift/proxy-server.conf:              
  file:
    - managed                              
    - source: salt://swift-proxy/proxy-server.conf
    - user: root
    - group: root
    - mode: 640
    - template: jinja
    - context:
        proxy_ip: {{ salt['network.interfaces']()['eth0']['inet'][0]['address'] }}
        storage_ip: {{ salt['network.ip_addrs']('eth0')[0] }}

