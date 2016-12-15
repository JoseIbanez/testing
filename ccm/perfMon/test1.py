from suds.client import Client
from suds import WebFault
from suds.transport.https import HttpAuthenticated
import os.path
import ssl
import time
import logging

logging.basicConfig(level=logging.CRITICAL)
logging.getLogger('suds.client').setLevel(logging.CRITICAL)
logging.getLogger('suds.transport').setLevel(logging.CRITICAL)
logging.getLogger('suds.xsd.schema').setLevel(logging.CRITICAL)
logging.getLogger('suds.wsdl').setLevel(logging.CRITICAL)


#context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context


#HOME = os.path.expanduser("")
HOME = os.path.dirname(os.path.abspath(__file__))



wsdl = "file://" + os.path.join(HOME, "wsdl/PerfmonService.xml")
cucm = "10.10.20.1"
cmport = "8443"
username = "administrator"
password = "ciscopsdt"
result_error = None
location = "https://" + cucm + ":" + cmport + "/perfmonservice2/services/PerfmonService/"
client = Client(wsdl,
                location=location,
                transport=HttpAuthenticated(username=username, password=password))

#result=client.service.perfmonListCounter()
#print result

session=client.service.perfmonOpenSession()
print session

ac=client.factory.create('RequestArrayOfCounterType')
c1=client.factory.create('CounterType')
c2=client.factory.create('CounterType')

c1.Name="\\\\hq-cucm-pub\\System\\IOPerSecond"
c2.Name="\\\\hq-cucm-sub1\\System\\IOPerSecond"
ac.Counter.append(c1)
ac.Counter.append(c2)

result=client.service.perfmonAddCounter(SessionHandle=session,ArrayOfCounter=ac)
print result

l=0
while (l<100):
    l+=1
    time.sleep(2)
    result=client.service.perfmonCollectSessionData(SessionHandle=session)
    print l, result[0].Value, result[1].Value


result=client.service.perfmonCloseSession(SessionHandle=session)
