#!/usr/bin/python

import re
import logging
from datetime import datetime



class Kpi(object):
    cmdFile="file"
    cmdName="test"
    reIn=":test in"
    reOut=":test out"

    @classmethod
    def hello(cls):
        return cls.cmdName

    @classmethod
    def isFile(cls,filename):
        if cls.cmdFile==filename:
            return True
        return False

    @classmethod
    def isCmd(cls,line):
        k=re.search(cls.reIn,line)
        #logging.debug(k)
        if k:
            logging.debug(line)
            logging.debug("Detect known cmd: "+cls.cmdName)
        return k


    def isOut(self,line):
        k=re.search(self.reOut,line)
        if k:
            self.inside=False
            self.finished=True
            logging.debug("Detect end of cmd: "+self.cmdName)
        return k


    def __init__(self):
        self.ret=0
        self.parse=False
        self.inside=False
        self.finished=False
        self.section=""
        self.kpi={}


    def __str__(self):
        return str(self.kpi)


    def parseLine(self,l):
        logging.debug(l)
        return 0

    def reset(self):
        self.__init__()
        self.inside=True





class ccmNtpStatus(Kpi):
    cmdFile="ntp.txt"
    cmdName="ccmNtpStatus"
    reIn=":utils ntp status"
    reOut="^admin:"


    def parseLine(self,line):

        if not self.inside:
            return False

        if self.isOut(line):
            return False

        if re.search("^synchronised.*stratum",line):
            logging.info("NTP synchronised")
            self.kpi['ccmNtpSynchronised']=1

        r=re.search("(?<=stratum )\d+",line)
        if r:
            logging.info("NTP Stratum "+r.group(0))
            self.kpi['ccmNtpStratum']=int(r.group(0))
            self.parse=True

        return True



class ccmLoad(Kpi):
    cmdFile="load.txt"
    cmdName="ccmLoad"
    reIn=":show process load"
    reOut="^admin:"

    def parseLine(self,line):
        logging.debug(line)

        if not self.inside:
            return False

        if self.isOut(line):
            return False

        r=re.search("(?<=load average: )\d+.\d+",line)
        if r:
            logging.info("Load average "+r.group(0))
            self.kpi['ccmLoadAVG1']=float(r.group(0))
            self.parse=True

        return True


class ccmStatus(Kpi):
    cmdFile="status.txt"
    cmdName="ccmStatus"
    reIn=":show status"
    reOut="^admin:"

    def parseLine(self,line):
        logging.debug(line)

        if not self.inside:
            return False

        if self.isOut(line):
            return False

        r=re.search("(?<=Free: ) +(\d+)K",line)
        if r:
            logging.info("Free Memory (0) "+r.group(0))
            logging.info("Free Memory (1) "+r.group(1))
            self.kpi['ccmFreeMemK']=int(r.group(1))
            self.parse=True


        r=re.search("(?<=Disk/active).+\((\d+)%\)",line)
        if r:
            logging.info("Used Disk/active "+r.group(1))
            self.kpi['ccmUsedDiskActiveP']=int(r.group(1))

        r=re.search("(?<=Disk/inactive).+\((\d+)%\)",line)
        if r:
            logging.info("Used Disk/inactive "+r.group(1))
            self.kpi['ccmUsedDiskInactiveP']=int(r.group(1))

        r=re.search("(?<=Disk/logging).+\((\d+)%\)",line)
        if r:
            logging.info("Used Disk/logging "+r.group(1))
            self.kpi['ccmUsedDiskLoggingP']=int(r.group(1))


        return True

class ccmDBreplication(Kpi):
    cmdFile="dbreplication.txt"
    cmdName="ccmDBreplication"
    reIn=":utils dbreplication runtimestate"
    reOut="^admin:"

    def __init__(self):
        super(ccmDBreplication, self).__init__()
        self.kpi['ccmDBreplicationOk']=0
        self.kpi['ccmDBreplicationError']=0

    def reset(self):
        super(ccmDBreplication, self).reset()
        self.kpi['ccmDBreplicationOk']=0
        self.kpi['ccmDBreplicationError']=0


    def parseLine(self,line):

        if not self.inside:
            return False

        if self.isOut(line):
            return False

        r=re.search("(?<=\().+\).+\((.)\)",line)
        if r:
            #logging.debug("Replication Status "+r.group(0))
            #logging.debug("Replication Status "+r.group(1))
            self.parse=True
            if (r.group(1) == "2"):
                self.kpi['ccmDBreplicationOk'] += 1
                logging.debug("Replication Status: OK, Nodes:"+str(self.kpi['ccmDBreplicationOk']))
            else:
                self.kpi['ccmDBreplicationError'] += 1
                logging.info("Replication Status: Error, Nodes:"+str(self.kpi['ccmDBreplicationError']))


        return True


class ccmPerfCCM(Kpi):
    cmdFile="perfCCM.txt"
    cmdName="ccmPerfCCM"
    reIn=":show perf query class \"Cisco CallManager\""
    reOut="^admin:"

    def parseLine(self,line):
        logging.debug(line)

        if not self.inside:
            return False

        if self.isOut(line):
            return False

        keyStrings=["CallsInProgress", 
                    "CallsAttempted",
                    "RegisteredHardwarePhones",
                    "CallsCompleted"]

        for string in keyStrings:
            r=re.search("(?<= -> "+string+").+= (\d+)",line)
            if r:
                logging.info(string+" "+r.group(1))
                self.kpi["ccm"+string]=int(r.group(1))
        
        r=re.search("(?<= -> CallsActive).+= (\d+)",line)
        if r:
            logging.info("CallsActive "+r.group(1))
            self.kpi['ccmCallsActive']=int(r.group(1))
            self.parse=True


        return True


