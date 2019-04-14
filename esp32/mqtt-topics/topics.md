
# Topic structure

cmd / deviceId [ . port ] [ / type ]


Cmds:
* b: Probe beacon, from probe to server
* r: Probe reading, from probe to server
* q: Order, from server to probe
* a: Answer, from probe to server after order


Reading types:
* "temp" Temperature
* "humi" Air humidity
* "mois" Moisture

# Examples

## Probe beacons
b/ESP0000000

## Probe readings 
r/ESP0000000.A0/temp  (value:)
r/ESP0000000.A3/mois  (value:)

## Probe query
q/ESP00000  (value: 1000;0001)

## Probe answer
a/ESP00000  (value: 1000;0001)

