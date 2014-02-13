kvm-pkgs:
  pkg.installed:
    - pkgs:
      - qemu-kvm 
      - libvirt-bin 
      - ubuntu-vm-builder 
      - bridge-utils
      - cloud-init
      - genisoimage
      - libcap2-bin

bridge-utils:
  pkg.installed


networking:
  service:
    - running
    - watch:
      - file: /etc/network/interfaces
    - require:
      - pkg: bridge-utils


/etc/network/interfaces:                            
  file:                                     
    - managed                              
    - source: salt://kvm/interfaces
