import json
from rn_vmanage import Vmanage


#vmanage_device = Device(auth, vmanage_host)
#device_config_list = vmanage_device.get_device_config_list('all')
#for device in device_config_list:
#    print(device)


vmanage = Vmanage()
vmanage.login()

try:
    print("get interface")
    result = vmanage.get_interface('10.245.9.103','ipv4')
    print(json.dumps(result,indent=2))
except:
    pass

#result = vmanage.get_statistics_approute()
#print("get approute")
#print(json.dumps(result,indent=2))

print("get events")
event_list = vmanage.get_events()

for event in event_list:
    print(event)
    #details = event.get('details')
    #print(details)



