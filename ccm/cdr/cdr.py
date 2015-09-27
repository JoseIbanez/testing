#!/usr/bin/python

# cat ./cmr_StandAloneCluster_01_20150421* | awk -F "\"*,\"*" '{print $3,$5,$7,$8,$10,$12,$13,$14,$18,$19}' | sort 
# "cdrRecordType","globalCallID_callManagerId","globalCallID_callId","nodeId","directoryNum","callIdentifier","dateTimeStamp","numberPacketsSent","numberOctetsSent","numberPacketsReceived","numberOctetsReceived","numberPacketsLost","jitter","latency","pkid","directoryNumPartition","globalCallId_ClusterID","deviceName","varVQMetrics"
# 0               1                             2                     3        4              5                6               7                   8                  9                       10                     11                  12       13        14     15                      16                      17                                                      


#"cdrRecordType","globalCallID_callManagerId","globalCallID_callId","origLegCallIdentifier","dateTimeOrigination","origNodeId","origSpan","origIpAddr","callingPartyNumber","callingPartyUnicodeLoginUserID","origCause_location","origCause_value","origPrecedenceLevel","origMediaTransportAddress_IP","origMediaTransportAddress_Port","origMediaCap_payloadCapability","origMediaCap_maxFramesPerPacket","origMediaCap_g723BitRate","origVideoCap_Codec","origVideoCap_Bandwidth","origVideoCap_Resolution","origVideoTransportAddress_IP","origVideoTransportAddress_Port","origRSVPAudioStat","origRSVPVideoStat","destLegIdentifier","destNodeId","destSpan","destIpAddr","originalCalledPartyNumber","finalCalledPartyNumber","finalCalledPartyUnicodeLoginUserID","destCause_location","destCause_value","destPrecedenceLevel","destMediaTransportAddress_IP","destMediaTransportAddress_Port","destMediaCap_payloadCapability","destMediaCap_maxFramesPerPacket","destMediaCap_g723BitRate","destVideoCap_Codec","destVideoCap_Bandwidth","destVideoCap_Resolution","destVideoTransportAddress_IP","destVideoTransportAddress_Port","destRSVPAudioStat","destRSVPVideoStat","dateTimeConnect","dateTimeDisconnect","lastRedirectDn","pkid","originalCalledPartyNumberPartition","callingPartyNumberPartition","finalCalledPartyNumberPartition","lastRedirectDnPartition","duration","origDeviceName","destDeviceName","origCallTerminationOnBehalfOf","destCallTerminationOnBehalfOf","origCalledPartyRedirectOnBehalfOf","lastRedirectRedirectOnBehalfOf","origCalledPartyRedirectReason","lastRedirectRedirectReason","destConversationId","globalCallId_ClusterID","joinOnBehalfOf","comment","authCodeDescription","authorizationLevel","clientMatterCode","origDTMFMethod","destDTMFMethod","callSecuredStatus","origConversationId","origMediaCap_Bandwidth","destMediaCap_Bandwidth","authorizationCodeValue","outpulsedCallingPartyNumber","outpulsedCalledPartyNumber","origIpv4v6Addr","destIpv4v6Addr","origVideoCap_Codec_Channel2","origVideoCap_Bandwidth_Channel2","origVideoCap_Resolution_Channel2","origVideoTransportAddress_IP_Channel2","origVideoTransportAddress_Port_Channel2","origVideoChannel_Role_Channel2","destVideoCap_Codec_Channel2","destVideoCap_Bandwidth_Channel2","destVideoCap_Resolution_Channel2","destVideoTransportAddress_IP_Channel2","destVideoTransportAddress_Port_Channel2","destVideoChannel_Role_Channel2","IncomingProtocolID","IncomingProtocolCallRef","OutgoingProtocolID","OutgoingProtocolCallRef","currentRoutingReason","origRoutingReason","lastRedirectingRoutingReason","huntPilotPartition","huntPilotDN","calledPartyPatternUsage","IncomingICID","IncomingOrigIOI","IncomingTermIOI","OutgoingICID","OutgoingOrigIOI","OutgoingTermIOI","outpulsedOriginalCalledPartyNumber","outpulsedLastRedirectingNumber","wasCallQueued","totalWaitTimeInQueue","callingPartyNumber_uri","originalCalledPartyNumber_uri","finalCalledPartyNumber_uri","lastRedirectDn_uri","mobileCallingPartyNumber","finalMobileCalledPartyNumber","origMobileDeviceName","destMobileDeviceName","origMobileCallDuration","destMobileCallDuration","mobileCallType","originalCalledPartyPattern","finalCalledPartyPattern","lastRedirectingPartyPattern","huntPilotPattern"
# 0               1                            2                     3                       4                     5            6          7            8                                          

import sys;
import csv;
import datetime;
import time;

def time_to_string(time_value):
    """convert Unix epoch time to a human readable string"""
    if not (time_value.isdigit()):
	return time_value

    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(time_value)))


def int_to_ip(signed_int):
    """ convert a 32-bit signed integer to an IP address"""
    # do preventative type checking because I didn't want to check inputs

    #if not (signed_int.isnumeric()):
    #    return signed_int



    try:
        if type(signed_int) == str or type(signed_int) == int:
            signed_int = long(signed_int)
    except ValueError:
        return signed_int

    # CUCM occasionally creates CDRs with an IP of '0'. Bug or feature? Beats me.
    if signed_int == 0:
        return "err_ip"
    
    # hex conversion for 32-bit signed int; 
    # the slice at the end removes the '0x' and 'L' in the result
    h = hex(signed_int & 0xffffffff)[2:-1] 

    if len(h) == 7: #pad initial zero if required
        h = '0' + h

    hex_ip = [h[6:8],h[4:6],h[2:4],h[:2]] # reverse the octets

    #put them back together in IPv4 format
    ip = '.'.join([str(int(n,16)) for n in hex_ip]) 

    return ip


#in_file = open("tmob_notcleaned.csv", "rb")
#reader = csv.reader(in_file)
reader = csv.reader(iter(sys.stdin.readline, ''))

row = 1
for row in reader:
  #print row[2], row[5], row[7]
  #if (row[4].isdigit()):
  #  row[4]=datetime.datetime.fromtimestamp(int(row[4])).strftime('%Y-%m-%d %H:%M:%S') 
  row[4]=time_to_string(row[4])  

  row[ 7]=int_to_ip(row[ 7])
  row[13]=int_to_ip(row[13])
  row[28]=int_to_ip(row[28])
  row[35]=int_to_ip(row[35])





  print ','.join([row[2],row[4],row[6],row[7],row[13],row[28],row[35],row[8],row[9],row[11],row[12]])  
  
  
