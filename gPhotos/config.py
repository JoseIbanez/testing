#!/usr/bin/env python
import json
import os


def getConfig(param):
    """
    Get configuration parameter
    1st try to find a ENV var
    2nd open the config file
    """

    param_env = param.replace(".","_").upper()

    #print(f"param: {param} / {param_env}")

    if os.environ.get(param_env):
        return os.environ.get(param_env)

    # Get config from file
    configFile = os.environ.get("CONFIGFILE") or "./config.json"

    try:
        with open(configFile) as json_file:
            config = json.load(json_file)   
    except:
        return None

    value = safeget(config,param.split("."))
    
    return value
    

def safeget(dct, keys):
    """
    Get a nested value in a json file
    Only nested dict is supported, no lists
    """
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct



if __name__ == "__main__":


    print(f"gphotos.album: {getConfig('gphotos.album')}")
    print(f"instagram.username: {getConfig('instagram.username')}")
    
