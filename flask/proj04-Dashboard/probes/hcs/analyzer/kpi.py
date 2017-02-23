#!/usr/bin/python

import re
import logging
from datetime import datetime
import nameAlias

class Kpi(object):

    def __init__(self,group,domain,name,value):
        self.group=group
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


    def addKpi(self,group,domain,name,value):
        item=Kpi(group,domain,name,value)
        logging.debug("Detected new kpi:"+str(item))
        self.kpiList.append(item)

    def printKpiList(self):
        nameAlias.objectAlias()

        for item in self.kpiList:
            logging.debug("Domain: "+str(item.domain))
            objItems=item.domain.split("/")
            logging.debug("Domain: "+str(objItems))

            objType=objItems[0]
            objOrgName=objItems[1]
            objName=nameAlias.objectAlias.search(objOrgName)
            logging.debug("Object: "+objType+", "+objOrgName+", "+objName)
            obj=nameAlias.canonicalName(self.host,objName)

            tags=[]

            tags.append("region="+str(obj.region))
            tags.append("dc="+str(obj.dc))
            tags.append("cust="+obj.region+str(obj.customer).zfill(3))
            tags.append("cluster="+str(obj.cluster))
            tags.append("device="+obj.device)
            tags.append(objType+"="+objName)

            if obj.function:
                tags.append("function="+obj.function)

            try:
                tags.append(objItems[2]+"="+objItems[3])
            except:
                logging.debug("not sub object")

            logging.debug(tags)

            value=item.name+"="+str(item.value)
            logging.debug(value)

            print(item.group+","+",".join(tags)+" "+value+" "+self.date.strftime("%s")+"000000000")


    def parseLine(self,l):
        logging.debug(l)
        return 0

    def reset(self):
        self.__init__()
        self.inside=True
