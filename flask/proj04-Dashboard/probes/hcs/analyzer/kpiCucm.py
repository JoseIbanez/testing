#!/usr/bin/python

import re
import logging
from datetime import datetime
import kpi

class ccmNtpStatus(kpi.Cmd):
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
            self.addKpi("ntp","node/"+self.host,"synchronised",1)

        r=re.search("(?<=stratum )\d+",line)
        if r:
            self.addKpi("ntp","node/"+self.host,"stratum",int(r.group(0)))
            self.parse=True

        return True



class ccmLoad(kpi.Cmd):
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
            self.addKpi("cpu","node/"+self.host+"/measure/AVG1","load",float(r.group(0)))
            self.parse=True

        return True


class ccmStatus(kpi.Cmd):
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
            self.addKpi("mem","node/"+self.host,"free",int(r.group(1)))
            self.parse=True

        r=re.search("(?<=Disk/active).+\((\d+)%\)",line)
        if r:
            self.addKpi("disk","node/"+self.host+"/Partition/Active","used",int(r.group(1)))

        r=re.search("(?<=Disk/inactive).+\((\d+)%\)",line)
        if r:
            self.addKpi("disk","node/"+self.host+"/Partition/Inactive","used",int(r.group(1)))

        r=re.search("(?<=Disk/logging).+\((\d+)%\)",line)
        if r:
            self.addKpi("disk","node/"+self.host+"/Partition/Logging","used",int(r.group(1)))

        return True

class ccmDBreplication(kpi.Cmd):
    cmdFile="dbreplication.txt"
    cmdName="ccmDBreplication"
    reIn=":utils dbreplication runtimestate"
    reOut="^admin:"

    def __init__(self):
        super(ccmDBreplication, self).__init__()
        self.ccmDBreplicationOk=0
        self.ccmDBreplicationError=0

    def reset(self):
        super(ccmDBreplication, self).reset()
        self.ccmDBreplicationOk=0
        self.ccmDBreplicationError=0


    def parseLine(self,line):

        if not self.inside:
            return False

        if self.isOut(line):
            self.addKpi("db","node/"+self.host+"Replication/Ok",   "counter", self.ccmDBreplicationOk)
            self.addKpi("db","node/"+self.host+"Replication/Error","counter", self.ccmDBreplicationError)
            return False

        logging.debug(line)

        r=re.search("(?<=\().+\).+\((.)\)",line)
        if r:
            self.parse=True
            if (r.group(1) == "2"):
                self.ccmDBreplicationOk += 1
                logging.debug("Replication Status: OK, Nodes:"+str(self.ccmDBreplicationOk))
            else:
                self.ccmDBreplicationError += 1
                logging.info("Replication Status: Error, Nodes:"+str(self.ccmDBreplicationError))


        return True


class ccmPerfCCM(kpi.Cmd):
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
            self.kpi['cust.ccm.cluster.datacentre.node.calls']=int(r.group(1))
            self.parse=True


        return True
