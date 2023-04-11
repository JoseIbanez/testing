import os
import json
from vmanage.api.device import Device
from vmanage.api.authentication import Authentication

from vmanage.api.http_methods import HttpMethods
from vmanage.data.parse_methods import ParseMethods
from vmanage.utils import list_to_dict


class Vmanage(object):

    def __init__(self, session, host, port=443):
        self.session = session
        self.host = host
        self.port = port
        self.base_url = f'https://{self.host}:{self.port}/dataservice/'


    def get_events(self):
        url = f"{self.base_url}event"

        payload = {
            "query": {
                "condition": "AND",
                "rules": [{
                    "value": [ "6" ],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "last_n_hours"
                    }]
                },
            "size": 10000
            }

        response = HttpMethods(self.session, url).request('POST', payload=json.dumps(payload))
        result = ParseMethods.parse_data(response)
        return result


    def get_interface(self,deviceId,af_type):
        url = f"{self.base_url}device/interface?deviceId={deviceId}&af-type={af_type}"

        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result


    def get_statistics_interface(self):
        #url = f"{self.base_url}statistics/interface"
        url = f"{self.base_url}statistics/approute"


        response = HttpMethods(self.session, url).request('GET')
        result = ParseMethods.parse_data(response)
        return result





vmanage_host = os.environ.get('VMANAGE_HOST')
vmanage_username = os.environ.get('VMANAGE_USERNAME')
vmanage_password = os.environ.get('VMANAGE_PASSWORD')
auth = Authentication(host=vmanage_host, user=vmanage_username, password=vmanage_password).login()


#vmanage_device = Device(auth, vmanage_host)
#device_config_list = vmanage_device.get_device_config_list('all')
#for device in device_config_list:
#    print(device)


vmanage = Vmanage(auth, vmanage_host)
#result = vmanage.get_interface('10.10.1.3','ipv4')
result = vmanage.get_statistics_interface()
print(json.dumps(result))

#event_list = vmanage_events.get_events()
#print(json.dumps(event_list))