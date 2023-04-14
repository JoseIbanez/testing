import json
import logging
from datetime import datetime,timezone


from common import configure_loger
from rn_vmanage import Vmanage


#vmanage_device = Device(auth, vmanage_host)
#device_config_list = vmanage_device.get_device_config_list('all')
#for device in device_config_list:
#    print(device)

logger = logging.getLogger(__name__)
configure_loger()

vmanage = Vmanage()
vmanage.login()

try:
    print("get interface")
    #result = vmanage.get_interface('10.245.9.103','ipv4')
    #print(json.dumps(result,indent=2))
except:
    pass

print("get approute")
result = vmanage.get_statistics_approute()
for event in result:

    print(event)
    entry_time = event.get('entry_time')
    #print(entry_time)
    print(datetime.fromtimestamp(entry_time/1000,tz=timezone.utc).isoformat())
    #details = event.get('details')
    #print(details)

print("get events")
#event_list = vmanage.get_events()

#for event in event_list:
#    print(event)
    #details = event.get('details')
    #print(details)


print("get events")
#event_list = vmanage.get_alarms()

#for event in event_list:
#    print(event)
    #details = event.get('details')
    #print(details)


