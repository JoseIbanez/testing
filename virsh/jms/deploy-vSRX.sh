virsh destroy vSRX
virsh undefine vSRX


virt-install --name vSRX --memory 4096 --cpu Westmere,+vmx,-invtsc --vcpus=2 \
        --arch=x86_64 \
        --graphics vnc,listen=0.0.0.0 --noautoconsole \
        --disk path=/var/lib/libvirt/images/j1.qcow2,size=16,device=disk,bus=ide,format=qcow2 \
        --os-type linux --os-variant rhel7 --import


  <cpu mode='custom' match='exact' check='partial'>
    <model fallback='allow'>SandyBridge</model>
    <vendor>Intel</vendor>
    <feature policy='require' name='vmx'/>
    <feature policy='disable' name='x2apic'/>
    <feature policy='disable' name='invtsc'/>
  </cpu>
  <graphics type='vnc' port='-1' autoport='yes'  listen='127.0.0.1' passwd='1234'/>
