#!/usr/bin/python

import re
import logging
from datetime import datetime

class superCmd:

    def __init__(self):
        self.cmdList=[]
        self.cmdList.append(ccmNtpStatus())
        self.cmdList.append(ccmLoad())

    def parseCmdPath(self,path):
        logging.debug("ParseCmdPath Input: "+path)
        pathParm=path.split("/")
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
        if self.cmdFile == "ntp.txt":
            return True
        if self.cmdFile == "load.txt":
            return True
        return False

    def parseCmdLine(self,line):

        if not self.cmd:
            for c in self.cmdList:
                if c.isCmd(line):
                    self.cmd=c
                    self.cmd.inside=True
                    self.cmd.finished=False
                    break
            return

        if not self.cmd:
            return

        self.cmd.parseLine(line)

        if not self.cmd.inside and self.cmd.finished:
            print self
            self.cmd=None

        return


    def __str__(self):
        return self.date.strftime("%Y-%m-%d %H:%M")+", "+self.host+", "+self.cmdFile+", "+str(self.cmd)







class Kpi:
    cmdName="test"
    reIn=":test in"
    reOut=":test out"

    @classmethod
    def hello(cls):
        return cls.cmdName

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
        self.inside=False
        self.finished=False
        self.section=""
        self.kpi={}

    def __str__(self):
        return str(self.kpi)

    def parseLine(self,l):
        logging.debug(l)
        return 0



class ccmNtpStatus(Kpi):
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

        return True



class ccmLoad(Kpi):

    cmdName="ccmLoad"
    reIn=":show process load"
    reOut="^admin:"

    def parseLine(self,line):
        logging.debug(line)
        if not self.inside and re.search("^show process load",line):
            self.inside=True
            logging.debug("Cmd Inside")
            return True

        if not self.inside:
            return False

        if self.isOut(line):
            return False

        r=re.search("(?<=load average: )\d+.\d+",line)
        if r:
            logging.info("Load average "+r.group(0))
            self.kpi['ccmLoadAVG1']=float(r.group(0))

        return True
