#!/bin/python

# cat ./cmr_StandAloneCluster_01_20150421* | awk -F "\"*,\"*" '{print $3,$5,$7,$8,$10,$12,$13,$14,$18,$19}' | sort 
# "cdrRecordType","globalCallID_callManagerId","globalCallID_callId","nodeId","directoryNum","callIdentifier","dateTimeStamp","numberPacketsSent","numberOctetsSent","numberPacketsReceived","numberOctetsReceived","numberPacketsLost","jitter","latency","pkid","directoryNumPartition","globalCallId_ClusterID","deviceName","varVQMetrics"
# 0               1                             2                     3        4              5                6               7                   8                  9                       10                     11                  12       13        14     15                      16                      17                                                      


import sys;
import csv;
import datetime;

#in_file = open("tmob_notcleaned.csv", "rb")
#reader = csv.reader(in_file)
reader = csv.reader(iter(sys.stdin.readline, ''))

row = 1
for row in reader:
  #print row[2], row[5], row[7]
  if (row[6].isdigit()):
    row[6]=datetime.datetime.fromtimestamp(int(row[6])).strftime('%Y-%m-%d %H:%M:%S') 
    

  print ','.join([row[2],row[4],row[6],row[7],row[9],row[11],row[12],row[13],row[17],row[18]])  
  
  