#!/usr/bin/env python

import json
import argparse
from ringcentral import SDK






def ring(config, recipient):

    RINGCENTRAL_CLIENTID =     config["RINGCENTRAL_CLIENTID"]
    RINGCENTRAL_CLIENTSECRET = config["RINGCENTRAL_CLIENTSECRET"]
    RINGCENTRAL_SERVER =       config["RINGCENTRAL_SERVER"]
    RINGCENTRAL_USERNAME =     config["RINGCENTRAL_USERNAME"]
    RINGCENTRAL_PASSWORD =     config["RINGCENTRAL_PASSWORD"]
    RINGCENTRAL_EXTENSION =    config["RINGCENTRAL_EXTENSION"]

    print(json.dumps(config))

    rcsdk = SDK( RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER)
    platform = rcsdk.platform()
    platform.login(RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD)

    resp = platform.post('/restapi/v1.0/account/~/extension/~/ring-out',
                {
                    'from' : { 'phoneNumber': RINGCENTRAL_USERNAME },
                    'to'   : {'phoneNumber': recipient},
                    'playPrompt' : False
                })
    print(f"Call placed. Call status: {resp.json().status.callStatus}")
    print(resp.json_dict())


def read_config(file_path):
    with open(file_path,"r") as json_file:
        return json.load(json_file)


def main():


    parser = argparse.ArgumentParser(
        description='RingCentral test')

    parser.add_argument(
        '-recipient',
        type=str,
        help='Calling to',
        default='+3491110000')

    args = parser.parse_args()


    config = read_config("./rc-credentials.json")
    ret = ring ( config, args.recipient)



if __name__ == '__main__':
    main()