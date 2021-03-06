from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError

host = '18.216.57.100'
user = 'root'
passwd = 'xxxx'
privateKey= 'altran-ohio.pem'
conf_file = 'configs/demo02.conf'

cmd='set groups aws-default system root-authentication plain-text-password-value Testing17'


def main():
    # open a connection with the device and start a NETCONF session
    try:
        dev = Device(host=host,user=user,ssh_private_key_file=privateKey)
        print ("Connecting...")
        dev.open()
        print ("Connected.")

        dev.bind(cu=Config)

        # Lock the configuration, load configuration changes, and commit
        print ("Locking the configuration")
        dev.cu.lock()

        print ("Loading configuration changes")
        #dev.cu.load(path=conf_file, merge=True)
        dev.cu.load(cmd, merge=True)

        print ("Diff")
        dev.cu.pdiff() 

        print ("Committing the configuration")
        dev.cu.commit(comment='Loaded by example.')

        print ("Unlocking the configuration")
        dev.cu.unlock()



    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))

    except LockError as err:
        print ("Unable to lock configuration: {0}".format(err))

    except (ConfigLoadError, Exception) as err:
        print ("Unable to load configuration changes: {0}".format(err))
        print ("Unlocking the configuration")
        try:
            dev.cu.unlock()
        except UnlockError:
            print ("Unable to unlock configuration: {0}".format(err))

    except CommitError as err:
        print ("Unable to commit configuration: {0}".format(err))
        print ("Unlocking the configuration")
        try:
            dev.cu.unlock()
        except UnlockError as err:
            print ("Unable to unlock configuration: {0}".format(err))

    except UnlockError as err:
        print ("Unable to unlock configuration: {0}".format(err))



    # End the NETCONF session and close the connection
    dev.close()



if __name__ == "__main__":
    main()