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

        if self.cmd == None:
            for c in self.cmdList:
                if c.isCmd(line):
                    self.cmd=c
                    self.cmd.inside=True
                    logging.debug(self.cmd)
                    break
            return

        if self.cmd == None:
            return

        self.cmd.parseLine(line)

        if not self.cmd.inside and self.cmd:
            print self.host+str(self.cmd.kpi)
            self.cmd=None

        return


    def __str__(self):
        return self.cust+", "+self.host+", "+self.cmdFile




class Kpi:

    @staticmethod
    def hello():
        return "hello"

    @staticmethod
    def isCmd(line):
        k=re.search("test cmd",line)
        logging.debug(k)
        if not k == None:
            return True
        return False


    def __init__(self):
        self.ret=0
        self.inside=0
        self.section=""
        self.kpi={}

    def __str__(self):
        return str(self.kpi)

    def parseLine(self,l):
        print(l)
        return 0



class ccmNtpStatus(Kpi):

    @staticmethod
    def isCmd(line):
        k=re.search(":utils ntp status",line)
        if not k == None:
            logging.debug("Detect known cmd: ccmNtpStatus")
        return k

    def parseLine(self,line):
        logging.debug(line)

        if not self.inside:
            return False

        if re.search("^admin:",line):
            self.inside=False
            logging.debug("Cmd End")
            return False


        if re.search("^synchronised.*stratum",line):
            logging.debug("NTP synchronised")
            self.kpi['ccmNtpSynchronised']=1


        r=re.search("(?<=stratum )\d+",line)
        if r:
            logging.debug("NTP Stratum "+r.group(0))
            self.kpi['ccmNtpStratum']=int(r.group(0))

        return True



class ccmLoad(Kpi):

    @staticmethod
    def isCmd(line):
        k=re.search(":show process load",line)
        logging.debug(k)
        if not k == None:
            logging.debug("Detect known cmd: ccmLoad")
            return True
        return False

    def parseLine(self,line):
        logging.debug(line)
        if not self.inside and re.search("^show process load",line):
            self.inside=True
            logging.debug("Cmd Inside")
            return True

        if not self.inside:
            return False

        if re.search("^admin:",line):
            self.inside=False
            logging.debug("Cmd End")
            return False


        r=re.search("(?<=load average: )\d+.\d+",line)
        if r:
            logging.debug("Load average "+r.group(0))
            self.kpi['ccmLoadAVG1']=float(r.group(0))

        return True
