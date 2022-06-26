
from device.device import NetconfDevice
from config.config import Config 
#import kafka
#import neo4j



def iterateOnDevices(): 

    config = Config()

    #kafkaConfig = getConfig(env,"kafkaConfig")
    #kafkaServer = kafkaServer(kafkaConfig)

    #neo4jConfig = getConfig(env,"neo4jConfig")
    #neo4jServer = Neo4jServer(neo4jConfig)

    #deviceList = neo4jServer.get_device_list(env,tenant)
    

    credentials = { "user": config.get(["netconf","credentials","user"]),
                    "password": config.get(["netconf","credentials","pass"])
                  }

    deviceList = [
        {"host":"1.1.1.1", "name":"device1"}
    ]

    for device in deviceList:
        print(f"device name {device['name']}")
        
        device = NetconfDevice(device,credentials)
        result = device.executeCommand("hi")
        print(result)   


def main():
    iterateOnDevices()

if __name__ == '__main__':
    main()