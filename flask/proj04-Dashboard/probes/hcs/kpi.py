#!/usr/bin/python

import re
import logging
from datetime import datetime

class superCmd:

    def __init__(self):
        self.cmdList=[]
        self.cmdList.append(ccmNtpStatus())
        self.cmdList.append(ccmLoad())
        self.cmdList.append(ccmStatus())
        self.cmdList.append(ccmDBreplication())

    def parseCmdPath(self,path):
        logging.debug("ParseCmdPath Input: "+path)
        pathParm=path.split("/")
        self.path=path
        self.fileName=pathParm[-1]
        self.date=datetime.strptime(pathParm[-2],'%Y%m%d-%H%M')
        self.lote=pathParm[-3]
        self.cust=pathParm[-4]
        pathParm=self.fileName.split("-",1)
        self.host=pathParm[0]
        self.cmdFile=pathParm[1]
        self.cmdType=None
        self.cmd=None
        logging.debug("ParseCmdPath Result: "+str(self))

    def knownCmd(self):
        for c in self.cmdList:
            if c.isFile(self.cmdFile):
                return True
        return False

    def parseCmdLine(self,line):

        if not self.cmd:
            for c in self.cmdList:
                if c.isCmd(line):
                    self.cmd=c
                    self.cmd.reset()
                    break
            return

        if not self.cmd:
            return

        self.cmd.parseLine(line)

        if not self.cmd.inside and self.cmd.finished:
            #print self
            self.toPrint()
            if not self.cmd.parse:
                logging.error(str(self.cmd.cmdName)+" not found in "+self.path)
            self.cmd=None

        return


    def __str__(self):
        return self.date.strftime("%Y-%m-%d %H:%M")+", "+self.host+", "+self.cmdFile+", "+str(self.cmd)

    def toPrint(self):
        for key,value in self.cmd.kpi.iteritems():
            myOutput=",".join([self.cust,key,self.host,str(value),str(self.date)])
            print(myOutput)





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
        logging.debug(k)
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
        logging.debug(line)

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


        r=re.search("(?<=Disk/active).+\((\d+)%\)",line)
        if r:
            logging.info("Used Disk/active "+r.group(1))
            self.kpi['ccmUsedDiskActiveP']=int(r.group(1))

        r=re.search("(?<=Disk/active).+\((\d+)%\)",line)
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
        logging.debug(line)

        if not self.inside:
            return False

        if self.isOut(line):
            return False

        r=re.search("(?<=\().+\).+\((.)\)",line)
        if r:
            logging.debug("Replication Status "+r.group(0))
            logging.debug("Replication Status "+r.group(1))
            self.parse=True
            if (r.group(1) == "2"):
                self.kpi['ccmDBreplicationOk'] += 1
                logging.debug("Replication Status: OK, Nodes:"+str(self.kpi['ccmDBreplicationOk']))
            else:
                self.kpi['ccmDBreplicationError'] += 1
                logging.info("Replication Status: Error, Nodes:"+str(self.kpi['ccmDBreplicationError']))


        return True
