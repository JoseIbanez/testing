ibanez@homer:~/Projects/testing/IoT/aws$ aws iot create-thing --thing-name "raspberry02"
{
    "thingArn": "arn:aws:iot:eu-west-1:306432991657:thing/raspberry02",
    "thingName": "raspberry02"
}





aws iot attach-principal-policy \
  --principal "arn:aws:iot:eu-west-1:306432991657:cert/c6fdecf3ca29e5523182e2abbc9c31b673800f125af09d45161ef2963768c393" \
  --policy-name "raspberry02"


aws iot attach-thing-principal \
  --thing-name "raspberry02" \
  --principal "arn:aws:iot:eu-west-1:306432991657:cert/c6fdecf3ca29e5523182e2abbc9c31b673800f125af09d45161ef2963768c393"



mosquitto_sub --cafile ./iot-root-ca.pem \
  --cert ./raspberry02.cert \
  --key  ./raspberry02.pem \
  -h ".iot.eu-west-1.amazonaws.com" -p 8883 \
  -q 1 -d -t topic/test -i clientid1 --insecure
