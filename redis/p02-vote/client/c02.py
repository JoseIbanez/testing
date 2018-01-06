#!/usr/bin/python
import httplib
import random
import argparse
import sys

#Get options
parser = argparse.ArgumentParser(
         description='Testing vote app')
 
parser.add_argument(
        '-port',
        type=int,
        help='port of server',
        default=8000)

parser.add_argument(
        '-host',
        type=str,
        help='server name/ip',
        default="localhost")

args = parser.parse_args()



#Color table
colorList = ["blue", "orange", "red", "green", "yellow" ]
colorSize = len(colorList)-1



#Connect with server
conn = httplib.HTTPConnection(args.host, args.port)

#initial request
conn.request("GET", "/")
r1 = conn.getresponse()
#print(r1.status, r1.reason)
print(r1.read())

#vote loop
count = 0
while count < 100 :
    count = count + 1

    nColor = random.randint(0, colorSize)

    conn.request("GET", "/v1/vote?color="+colorList[nColor])
    r1 = conn.getresponse()
    #print(r1.read())

print

# view current results
conn.request("GET", "/v1/listVotes")
r1 = conn.getresponse()
print(r1.read())

conn.request("GET", "/v1/listWorkers")
r1 = conn.getresponse()
print(r1.read())


conn.close()