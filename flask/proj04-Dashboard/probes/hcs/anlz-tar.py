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

    parser.add_argument("-t", "--tar",  metavar="STRING", help="Tar file to parser",
                        default="~/Downloads/hc.sample.tgz")
    parser.add_argument("-f", "--filter", metavar="STRING", help="Filer to path",
                        default="")

    parser.add_argument("--debug", nargs='?', help="Enable debug",
                        default="")
    args = parser.parse_args()

    if (args.debug is None):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug active.")
    else:
        logging.basicConfig(level=logging.INFO)


    sc=kpi.superCmd()
    srcFile=args.tar
    line=0
    with tarfile.open(expanduser(srcFile)) as tar:
        for tarinfo in tar:
            line=line+1
            if line > 20000000000:
                logging.debug("Stop")
                break
            if not tarinfo.isreg():
                #logging.debug(tarinfo.name+" no regular file")
                continue

            if args.filter and args.filter!=tarinfo.name:
                continue

            sc.parseCmdPath(tarinfo.name)
            if not sc.knownCmd():
                continue
            logging.info(sc.cmdFile+","+sc.host)
            f=tar.extractfile(tarinfo)
            for l in f:
                cmdLine=l.strip('\n').strip('\r').rstrip(' ')
                if args.filter and args.filter==tarinfo.name:
                    logging.debug(cmdLine)

                sc.parseCmdLine(cmdLine)


if __name__ == "__main__":
    main()
