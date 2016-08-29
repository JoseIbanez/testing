#!/bin/bash

tmp="/tmp/pass.$1.xml"
export tmp

cp soapUpdateUserPassword.xml $tmp
sed -i "s/{{user}}/$1/g" $tmp
sed -i "s/{{pass}}/$2/g" $tmp

curlp () {
ipaddr=$@
echo
echo $ipaddr
curl -k -n  --interface eth2 -H "Content-type: text/xml;" -H "SOAPAction:CUCM:DB ver=8.5" -d @$tmp https://$ipaddr:8443/axl/
echo
}
export -f curlp


#xargs -0 -n 1 -P 8 -I param bash -c "file_process param" > /dev/null 2>&1

cat ./nodes.lst | xargs -n 1 -I ipaddr  bash -c "curlp ipaddr"

rm $tmp

