import json
from rn_vmanage import Vmanage


#vmanage_device = Device(auth, vmanage_host)
#device_config_list = vmanage_device.get_device_config_list('all')
#for device in device_config_list:
#    print(device)


vmanage = Vmanage()


result = vmanage.get_interface('10.10.1.3','ipv4')
print("get interface")
print(json.dumps(result[0],indent=2))


result = vmanage.get_statistics_approute()
print("get approute")
print(json.dumps(result[0],indent=2))

event_list = vmanage.get_events()
print("get events")
print(json.dumps(event_list[0],indent=2))

