from __future__ import (absolute_import, division, print_function)

import requests
import os
import urllib3
from datetime import datetime,timedelta,timezone
import logging
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

STANDARD_HEADERS = {'Connection': 'keep-alive', 'Content-Type': 'application/json'}
STANDARD_TIMEOUT = 10

logger = logging.getLogger(__name__)

class Vmanage(object):

    def __init__(self,validate_certs=False, timeout=STANDARD_TIMEOUT):

        self.username = os.environ.get('VMANAGE_USERNAME')
        self.password = os.environ.get('VMANAGE_PASSWORD')
        self.session = requests.session()
        self.session.verify = validate_certs

        proxy = os.environ.get('VMANAGE_PROXY')
        if proxy:
            self.session.proxies = { "http":proxy, "https":proxy} 

        url = os.environ.get('VMANAGE_URL')
        if url:
            self.base_url = f"{url}/dataservice/"
        else:
            host = os.environ.get('VMANAGE_HOST')
            port = int(os.environ.get('VMANAGE_PORT',443))    
            self.base_url = f'https://{host}:{port}/dataservice/'

        self.timeout = STANDARD_TIMEOUT





    def request(self, method, api, params=None, headers=None, payload=None, files=None, timeout=STANDARD_TIMEOUT):
        """Performs HTTP REST API Call.

        Args:
            method (str): DELETE, GET, POST, PUT
            headers (dict): Use standard vManage header provided in
                module or custom header for specific API interaction
            payload (str): A formatted string to be delivered to
                vManage via POST or PUT REST call
            file (obj): A file to be sent to vManage

        Returns:
            result (dict): A parsable dictionary containing the full
                response from vManage for an interaction

        Raises:
            JSONDecodeError: Payload format error.
            ConnectionError: Connection error.
            HTTPError: An HTTP error occurred.
            URLRequired: A valid URL is required to make a request.
            TooManyRedirects: Too many redirects.
            Timeout: The request timed out.
            RequestException: There was an ambiguous exception.

        """

        error = None
        data = None
        details = None
        body_json = None
        result_json = None
        if headers is None:
            headers = STANDARD_HEADERS

        if payload:
            if isinstance(payload, str):
                data = payload.replace("\'", "\"")
            elif isinstance(payload, dict):
                body_json=payload
            else:
                data = payload

        if files:
            headers = None

        url = self.base_url+api
        response = self.session.request(method, url, headers=headers,  params=params, json=body_json, files=files, data=data, timeout=timeout)


        try:
            result_json = response.json()
        except requests.exceptions.JSONDecodeError:
            result_json = None



        if response.status_code > 299:
            if result_json and 'error' in result_json:
                details = result_json['error']['details']
                error = result_json['error']['message']
                raise requests.exceptions.HTTPError(f"{url}: Error {response.status_code}: {error}: {details}")
            else:
                raise requests.exceptions.HTTPError(f"{url}: Error {response.status_code} ({response.text})")


        if result_json is None or not 'data' in result_json:
            raise requests.exceptions.HTTPError(f'{url}: Not data in answer: {response.text}')

        out_data = result_json.get('data')

        n_items = len(out_data) if isinstance(out_data,list) else 1
        logger.info("Query %s, duration:%s secs, items:%d, total size:%d bytes",url,response.elapsed.total_seconds(), n_items,len(response.text))

        return out_data



    def login(self):
        """Executes login tasks against vManage to retrieve token(s).

        Args:
            None.

        Returns:
            self.session: a Requests session with JSESSIONID and an
            X-XSRF-TOKEN for vManage version >= 19.2.0.

        Raises:
            LoginFailure: If the username/password are incorrect.
            RequestException: If the host is not accessible.

        """

        try:
            api = 'j_security_check'
            data={
                    'j_username': self.username,
                    'j_password': self.password
                }
 
            response = self.session.post(url=self.base_url+api,data=data,timeout=self.timeout)

            if (response.status_code != 200 or response.text.startswith('<html>')):
                raise ConnectionError('Login failed, check user credentials.')

            version = self.get_vmanage_version() 
            if version >= '19.2.0':
                api = 'client/token'
                response = self.session.get(url=self.base_url+api, timeout=self.timeout)
                self.session.headers['X-XSRF-TOKEN'] = response.content

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f'Could not connect to {self.base_url}: {e}')

        return self.session


    def get_vmanage_version(self):

        params = { 'model':'vmanage'}
        result = self.request('GET','system/device/controllers',params=params)

        version = result[0]['version']
        logger.info("Vmanage:%s Version:%s",self.base_url,version)
        return version



    def get_events(self):

        payload = {
            "query": {
                "condition": "AND",
                "rules": [{
                    "value": [ "24" ],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "last_n_hours"
                    }]
                },
            "size": 10000
            }

        result = self.request('POST',"event", payload=payload)
        return result


    def get_alarms(self):

        payload = {
            "query": {
                "condition": "AND",
                "rules": [{
                    "value": [ "2" ],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "last_n_hours"
                    }]
                },
<<<<<<< HEAD
            "size": 10
=======
            "size": 10000
>>>>>>> cb608f0bfd1fad405411a3fe5c1e565c4ddc3dee
            }

        result = self.request('POST',"alarms", payload=payload)
        return result



    def get_interface(self,deviceId,af_type):

        params = {
            'deviceId': deviceId
        }

        result = self.request('GET','device/interface',params=params)
        return result


    def get_statistics_approute(self,host_name:str):

        date_to   = datetime.now(timezone.utc)
        date_from = date_to - timedelta(minutes=30)

        payload = {
            "size": 10000,
            "query": {
                "condition": "AND",
                "rules": [{
                    "value": [ date_from.isoformat(), date_to.isoformat() ],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "between"
                    },{
                    "value": [ host_name ],
                    "field": "host_name",
                    "type": "string",
                    "operator": "equal"
                    }]
                },
            "sort":[{
                "field": "entry_time",
                "type": "date",
                "order": "asc"
            }],
            }

        result = self.request('POST',"statistics/approute",payload=payload)
        return result

    def get_devices(self):
        result = self.request('GET','device')
        return result

    def get_topology(self):
        result = self.request('GET','topology')
        return result
