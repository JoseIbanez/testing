#!/usr/bin/python

import re
import logging
from datetime import datetime

class superCmd:

    def __init__(self):
        self.cmdList=[]


    def parseNodeAlias(self,path):
        newPath=path
        for a in self.aliasList:
            logging.debug("parseNodeAlias, alias:"+a.alias+", path:"+path)
            newPath=re.sub(a.alias,a.canonical,path)
            if path!=newPath:
                logging.debug("New path: "+newPath)
                break

        return newPath


    def parseCmdPath(self,path):
        logging.debug("ParseCmdPath Input: "+path)
        path=self.parseNodeAlias(path)
        try:
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
            return True
        except:
            logging.error("Path parse error:"+path)
        return False


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
            self.toPrint()
            if not self.cmd.parse:
                logging.error(str(self.cmd.cmdName)+" not found in "+self.path)
            self.cmd=None

        return


    def __str__(self):
        return self.date.strftime("%Y-%m-%d %H:%M")+", "+self.host+", "+self.cmdFile+", "+self.cust


    def toPrint(self):
        for key,value in self.cmd.kpi.iteritems():
            myOutput=",".join([self.cust,key,self.host,str(value),str(self.date)])
            print(myOutput)


class nodeAlias(object):

    def __init__(self,alias,canonical):
        self.canonical=canonical
        self.alias=alias
        self.re=re.compile(alias)

