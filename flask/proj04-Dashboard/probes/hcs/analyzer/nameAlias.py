#!/usr/bin/python

import re
import logging
import csv

class aliasItem(object):
    alias=None
    canonical=None
    rePath=None
    reDomain=None

    def __init__(self,alias,canonical):
        self.alias=alias
        self.canonical=canonical
        self.rePath=re.compile("/"+alias)
        self.reDomain=re.compile("^"+alias)


class canonicalName(object):

    def __init__(self,type,cname):
        self.region=None
        self.dc=None
        self.function=None
        self.cluster=None
        self.customer=None
        self.type=type

        try:

            if type=="CUCM":
                self.region=cname[0:3]
                self.dc=cname[3:6]
                self.function=cname[6:8]
                self.cluster=cname[8:10]
                self.customer=cname[10:13]

            if type=="Net":
                self.region=cname[0:3]
                self.dc=cname[3:6]
                self.function=cname[6:8]
                self.cluster=""
                self.customer=""
            
            if type=="Adj":
                self.region=""
                self.dc=""
                self.function=""
                self.customer=""
                self.cluster=""

                r=re.search("(?<=CUCM-cust)(\d+)-\d+-CL(\d+)",cname)
                if r:
                    logging.debug("Adj:"+cname)
                    logging.debug("re:"+r.group(0))
                    logging.debug("Cust:"+r.group(1))
                    logging.debug("CL:"+r.group(2))
                    self.function="CUCM"
                    self.customer=r.group(1)
                    self.cluster=r.group(2)

                r=re.search("(?<=CUCM-cust)(\d+)-\d+$",cname)
                if r:
                    logging.debug("Adj:"+cname)
                    logging.debug("re:"+r.group(0))
                    logging.debug("Cust:"+r.group(1))
                    self.function="CUCM"
                    self.customer=r.group(1)
                    self.cluster="1"

                r=re.search("(?<=IMS-SPE)(\d+)-C(\d+)-CL(\d+)",cname)
                if r:
                    logging.debug("Adj:"+cname)
                    logging.debug("re:"+r.group(0))
                    logging.debug("Cust:"+r.group(2))
                    logging.debug("CL:"+r.group(3))
                    self.function="IMS"
                    self.customer=r.group(2)
                    self.cluster=r.group(3)

                    



            logging.debug("Name:"+cname+", Region:"+self.region+", Dc:"+self.dc+
                    ", Function:"+self.function+
                    ", Cluster:"+self.cluster+", Customer:"+self.customer) 



        except:
            logging.error("Wrong C.Name: "+cname)





class deviceAlias(object):
    aliasList=[]

    @classmethod
    def load(cls,filename):
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                try:
                    cls.addItem(row[0],row[1])
                    logging.debug("Added: "+row[0]+","+row[1])
                except:
                    logging.debug("Error "+str(row))
        return


    @classmethod
    def addItem(cls,alias,canonical):
        cls.aliasList.append(aliasItem(alias,canonical))
        return

    @classmethod
    def replace(cls,line):
        return

    @classmethod
    def replaceAliasPath(cls,path):
        newPath=path

        for a in cls.aliasList:
            newPath=a.rePath.sub("/"+a.canonical,path)
            if path!=newPath:
                logging.debug("New path: "+newPath)
                break

        return newPath


    @classmethod
    def search(cls,alias):
        newName=alias
        for a in cls.aliasList:
            if a.alias==alias:
                newName=a.canonical
                logging.debug("New Name: "+newName)
                break
        return newName



########################################################################################

class adjacencyAlias(object):
    aliasList={}

    @classmethod
    def __init__(cls):
        cls.load("../inventory/alias-adjacency.csv")


    @classmethod
    def load(cls,filename):
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                try:
                    cls.addItem(row[0],row[1])
                    logging.debug("Added: "+row[0]+","+row[1])
                except:
                    logging.debug("Error "+str(row))
        return


    @classmethod
    def addItem(cls,alias,canonical):
        cls.aliasList[alias]=canonical
        return

    @classmethod
    def search(cls,alias):
        try:
            newName=cls.aliasList[alias]
            logging.debug("Found Alias:"+alias+", C.Name"+newName)
        except:
            newName=alias
        return newName


###########################################################################################


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Debug active.")

    alias=deviceAlias()
    alias.load("../inventory/alias-device.csv")

    print(alias.search("cube2-grl"))
    print(alias.replaceAliasPath("s/s/cube1-swi-33.txt"))


    c1=canonicalName("CUCM","UKXSW1U200016")
    c2=canonicalName("CUCM","UKXLS2T202016")
    c2=canonicalName("Net","UKXLS2SB02")

    c3=canonicalName("Adj","CUCM-cust017-5-CL2")
    c3=canonicalName("Adj","CUCM-cust035-2")
    c3=canonicalName("Adj","IMS-SPE1-C001-CL2")


    adjAlias=adjacencyAlias()
    adjAlias.load("../inventory/alias-adjacency.csv")

    print(adjAlias.search("CUCM-cust035-2"))
    print(adjAlias.search("CUCM-cust161-3"))

    print(adjAlias.search("cust16"))




if __name__ == "__main__":
    main()


