import json
import logging
from datetime import datetime,timezone


from common import configure_loger
from rn_vmanage import Vmanage

#from vmanage.api.utilities


logger = logging.getLogger(__name__)
configure_loger()


def list_interface(vmanage:Vmanage):
    try:
        print("get interface")
        #result = vmanage.get_interface('10.245.9.103','ipv4')
        #print(json.dumps(result,indent=2))
    except:
        pass


def list_approute(vmanage:Vmanage,host_name:str):
    print("get approute")
    result = vmanage.get_statistics_approute(host_name)
    for event in result:

        print(json.dumps(event))
        #entry_time = event.get('entry_time')
        #print(entry_time)
        #print(datetime.fromtimestamp(entry_time/1000,tz=timezone.utc).isoformat())
        #details = event.get('details')
        #print(details)



def list_events():

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


def list_devices(vmanage:Vmanage):

    device_list = vmanage.get_devices()
    for device in device_list:
        print(json.dumps(device))


def list_topology(vmanage:Vmanage):
    topology = vmanage.get_topology()
    print(json.dumps(topology))


vmanage = Vmanage()
vmanage.login()

#list_devices(vmanage)
#list_approute(vmanage,"VF0050-5002")
list_topology(vmanage)