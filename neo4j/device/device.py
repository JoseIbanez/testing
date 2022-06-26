from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.exception import ConnectError

class NetconfDevice:
    """
    Handle juniper devices
    """    

    def __init__(self, config, credentials):
        print(config)
        print(credentials)
        self.host = config['host']
        self.user = credentials['user']
        self.password = None #credentials['pass']
        self.device = None
        self.shell = None
        self.open()



    def open(self):

        if self.device:
            return self.device

        try:
            self.device = Device(host=self.host,
                        user = self.user,
                        password = self.password)
            self.device.open()
            self.shell = StartShell(self.device)
            version = self.shell.run('cli -c "show version"')
            print(version)


        except ConnectError as err:
            print ("Cannot connect to device: {0}".format(err))
            return None

        except Exception as err:
            print(err)
            return None

        finally:
            self.shell and self.shell.close
            self.device and self.device.close
            self.shell = None
            self.device = None


    def close(self):
        self.sell and self.shell.close
        self.device and self.device.close


    def executeCommand(self, cmd):

        if not self.shell:
            print("No connected")
            return None

        result = None
        try:
            result = self.shell.run('cli -c "show version"')

        except Exception as err:
            print(f"error: {err}")


        return result




