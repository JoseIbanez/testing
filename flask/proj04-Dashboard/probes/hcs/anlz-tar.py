#!/usr/bin/python

import tarfile
import sys
from datetime import datetime
from os.path import expanduser
import re
import logging
import argparse
import kpi
import kpiCucm
import kpiCube
import superCmd

def lookforKnownCmd(line):
    k=re.search(":utils ntp status",line)
    if not k == None:
        logging.debug(k)
    return


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--tar",  metavar="STRING", help="Tar file to parser",
                        default="")
    parser.add_argument("-f", "--filter", metavar="STRING", help="Filer to path",
                        default="")

    parser.add_argument("-n", "--name", metavar="STRING", help="Simulated path",
                        default="")

    parser.add_argument("--debug", nargs='?', help="Enable debug",
                        default="")

    args = parser.parse_args()

    if (args.debug is None):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug active.")
    else:
        #logging.basicConfig(level=logging.INFO)
        logging.basicConfig(level=logging.ERROR)




    sc=superCmd.superCmd()
    sc.cmdList.append(kpiCucm.ccmNtpStatus())
    sc.cmdList.append(kpiCucm.ccmLoad())
    sc.cmdList.append(kpiCucm.ccmStatus())
    sc.cmdList.append(kpiCucm.ccmDBreplication())
    #sc.cmdList.append(kpiCucm.ccmPerfCCM())

    sc.cmdList.append(kpiCube.cubeCallStatCurrentDay())


    sc.aliasList=[]
    sc.aliasList.append(superCmd.nodeAlias("ucs1-swi","UKXSWIFI03"))
    sc.aliasList.append(superCmd.nodeAlias("ucs1-grl","UKXLS2FI03"))
    sc.aliasList.append(superCmd.nodeAlias("ucs2-grl","UKXLS2FI06"))

    sc.aliasList.append(superCmd.nodeAlias("cube1-grl","UKXLS2SB01"))
    sc.aliasList.append(superCmd.nodeAlias("cube1-swi","UKXSWISB01"))
    sc.aliasList.append(superCmd.nodeAlias("cube2-grl","UKXLS2SB02"))
    sc.aliasList.append(superCmd.nodeAlias("cube2-swi","UKXSWISB02"))



    #Tar mode
    if args.tar:
        srcFile=expanduser(args.tar)
        numFile=0
        with tarfile.open(srcFile) as tar:
            for tarinfo in tar:

                numFile=numFile+1
                if numFile > 20000000000:
                    logging.debug("Stop. numFile:"+str(numFile))
                    break

                if not tarinfo.isreg():
                    continue
                if not sc.parseCmdPath(tarinfo.name):
                    continue
                if not sc.knownCmd():
                    continue
                logging.info(sc.cmdFile+","+sc.host)

                f=tar.extractfile(tarinfo)
                for l in f:
                    cmdLine=l.strip('\n').strip('\r').rstrip(' ')
                    sc.parseCmdLine(cmdLine)

        logging.debug("End of tar, numFile:"+str(numFile))


    #Stdin Mode
    if args.name:
        if not sc.parseCmdPath(args.name):
            sys.exit()
        if not sc.knownCmd():
            sys.exit()
        logging.info(sc.cmdFile+","+sc.host)
        f=sys.stdin
        for l in f:
            cmdLine=l.strip('\n').strip('\r').rstrip(' ')
            sc.parseCmdLine(cmdLine)




if __name__ == "__main__":
    main()
