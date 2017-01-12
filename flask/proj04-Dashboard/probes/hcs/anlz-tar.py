#!/usr/bin/python

import tarfile
from datetime import datetime
from os.path import expanduser
import re
import logging
import argparse
import kpi

def lookforKnownCmd(line):
    k=re.search(":utils ntp status",line)
    if not k == None:
        logging.debug(k)
    return


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--section",  metavar="STRING", help="String to match in section header", default="")
    parser.add_argument("-c", "--child", metavar="STRING", help="String to match inside section", default="")
    parser.add_argument("--debug", nargs='?', help="Enable debug", default="")
    args = parser.parse_args()

    if (args.debug is None):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug active.")

    srcFile="~/Downloads/hc.sample.tgz"
    line=0
    sc=kpi.superCmd()

    with tarfile.open(expanduser(srcFile)) as tar:
        for tarinfo in tar:
            line=line+1
            if line > 20000:
                logging.debug("Stop")
                break

            if not tarinfo.isreg():
                logging.debug(tarinfo.name+" no regular file")
                continue

            sc.parseCmdPath(tarinfo.name)

            if not sc.knownCmd():
                continue

            print sc.cmdFile,sc.host


            f=tar.extractfile(tarinfo)
            for l in f:
                cmdLine=l.strip('\n').strip('\r').rstrip(' ')
                sc.parseCmdLine(cmdLine)



if __name__ == "__main__":
    main()
