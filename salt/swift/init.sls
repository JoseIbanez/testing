switf-proxy:
  pkg.installed:
    - pkgs:
      - memcached
      - screen


/etc/swift/proxy-server.conf:              
  file:
    - managed                              
    - source: salt://swift/proxy-server.conf
    - user: root
    - group: root
    - mode: 640
    - template: jinja
    - context:
        proxy_ip: {{ salt['network.interfaces']()['eth0']['inet'][0]['address'] }}
        storage_ip: {{ salt['network.ip_addrs']('eth0')[0] }}

