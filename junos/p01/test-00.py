from jnpr.junos import Device
from jnpr.junos.utils.config import Config
#from myTables.ConfigTables import ServicesConfigTable

dev = Device(host='192.168.1.80',user='root',password='Calor17').open()

with Config(dev, mode='private') as cu:    
    cu.load('set system services netconf ssh', format='set')
    #cu.load('set system services netconf traceoptions file test.log', format='set')

    new_User='set system login user Read class read-only authentication plain-text-password-value Read1234'
    cu.load(new_User, format='set')


    cu.pdiff()
    cu.commit()




#with ServicesConfigTable(dev, mode='private') as sct:
#    sct.ftp = True
#    sct.ssh = True
#    sct.telnet = True
#    sct.append()
#    sct.load()
#    sct.pdiff()
#    sct.commit()

