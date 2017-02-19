#!/usr/bin/python

import re
import logging
from datetime import datetime

class Kpi(object):

    def __init__(self,domain,name,value):
        self.domain=domain
        self.name=name
        self.value=value

    def __str__(self):
        return self.domain+","+self.name+","+str(self.value)



class Cmd(object):
    cmdFile="file"
    cmdName="test"
    reIn=":test in"
    reOut=":test out"

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
        self.kpiList=[]

    def __str__(self):
        return str(self.kpi)


    def addKpi(self,domain,name,value):
        item=Kpi(domain,name,value)
        logging.debug("Detected new kpi:"+str(item))
        self.kpiList.append(item)


    def parseLine(self,l):
        logging.debug(l)
        return 0

    def reset(self):
        self.__init__()
        self.inside=True
