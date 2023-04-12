from __future__ import (absolute_import, division, print_function)

import requests
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


STANDARD_HEADERS = {'Connection': 'keep-alive', 'Content-Type': 'application/json'}
STANDARD_TIMEOUT = 10


class Vmanage(object):

    def __init__(self,validate_certs=False, timeout=STANDARD_TIMEOUT):

        self.host = os.environ.get('VMANAGE_HOST')
        self.port = int(os.environ.get('VMANAGE_PORT',443))
        self.username = os.environ.get('VMANAGE_USERNAME')
        self.password = os.environ.get('VMANAGE_PASSWORD')
        self.session = requests.session()
        self.session.verify = validate_certs

        proxy = os.environ.get('VMANAGE_PROXY')
        if proxy:
            self.session.proxies = { "http":proxy, "https":proxy} 

        self.base_url = f'https://{self.host}:{self.port}/dataservice/'
        self.timeout = STANDARD_TIMEOUT


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

        result = self.request('POST',url, payload=payload)
        return result


    def get_interface(self,deviceId,af_type):
        url = f"{self.base_url}device/interface"

        params = {
            'deviceId': deviceId
        }

        result = self.request('GET',url,params=params)
        return result


    def get_statistics_approute(self):
        #url = f"{self.base_url}statistics/interface"
        url = f"{self.base_url}statistics/approute"

        payload = {
            "size": 10,
            "query": {
                "condition": "AND",
                "rules": [{
                    "value": [ "1" ],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "last_n_hours"
                    }]
                }
            }


        result = self.request('POST',url,payload=payload)
        return result




    def request(self, method, url, params=None, headers=None, payload=None, files=None, timeout=STANDARD_TIMEOUT):
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

        if headers is None:
            headers = STANDARD_HEADERS

        error = None
        data = None
        details = None
        body_json = None
        result_json = None

        if payload:
            if isinstance(payload, str):
                data = payload.replace("\'", "\"")
            elif isinstance(payload, dict):
                body_json=payload
            else:
                data = payload

        if files:
            headers = None


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



        if not 'data' in result_json:
            raise requests.exceptions.HTTPError(f'{self.url}: Not data in answer: {result_json}')


        return result_json.get('data')



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
            url = f'{self.base_url}{api}'


            response = self.session.post(url=url,
                                         data={
                                             'j_username': self.username,
                                             'j_password': self.password
                                         },
                                         timeout=self.timeout)

            if (response.status_code != 200 or response.text.startswith('<html>')):
                raise ConnectionError('Login failed, check user credentials.')

            #version = Utilities(self.session, self.host, self.port).get_vmanage_version()
            version = '19.2.0'

            if version >= '19.2.0':
                api = 'client/token'
                url = f'{self.base_url}{api}'
                response = self.session.get(url=url, timeout=self.timeout)
                self.session.headers['X-XSRF-TOKEN'] = response.content

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f'Could not connect to {self.host}: {e}')

        return self.session
