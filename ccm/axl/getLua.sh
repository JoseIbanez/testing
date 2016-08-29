#!/bin/bash

curlp () {
ipaddr=$@
echo
echo $ipaddr
curl --interface eth2 -k -n -H "Content-type: text/xml;charset=UTF-8" -H "SOAPAction:CUCM:DB ver=9.1" -d @./soapGetLuaInfo.xml https://$ipaddr:8443/axl/
echo
echo
curl --interface eth2 -k -n -H "Content-type: text/xml;charset=UTF-8" -H "SOAPAction:CUCM:DB ver=9.1" -d @./soapListTrunk.xml https://$ipaddr:8443/axl/
echo
echo
curl --interface eth2 -k -n -H "Content-type: text/xml;charset=UTF-8" -H "SOAPAction:CUCM:DB ver=9.1" -d @./soapGetTrunk.xml https://$ipaddr:8443/axl/

}
export -f curlp



curlp $1



