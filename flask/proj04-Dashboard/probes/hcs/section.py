#!/usr/bin/python
import sys
import re
import logging
import argparse
def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--name",  metavar="STRING", help="String to match in section header", default="")
    parser.add_argument("-c", "--child", metavar="STRING", help="String to match inside section", default="")
    parser.add_argument("--debug", nargs='?', help="Enable debug", default="")
    args = parser.parse_args()

    if (args.debug is None):
        logging.basicConfig(level=logging.DEBUG)

    logging.debug("Parameter name:"+args.name)
    section=args.name

    logging.debug("Parameter child:"+args.child)
    child=args.child


    deepn=0;
    deep=""
    inside=False
    sectionName=""

    beginRe = re.compile(section)
    insideRe = re.compile("")
    childRe = re.compile(child)


    for line in sys.stdin:

        if (inside and not re.match(insideRe,line)):
            logging.debug("Exit match")
            logging.debug(line.rstrip())
            inside=False

            if child and not foundChild:
                print(sectionName+" ; ")



        if ( not inside and re.search(beginRe,line.lstrip())):
            inside=True
            deepn=len(line)-len(line.lstrip())
            deep=" "* (deepn+1)
            sectionName=line.rstrip()
            foundChild=False
            insideRe = re.compile(deep)
            logging.debug("Match, deep:"+str(deepn)+" >"+deep+"<")


        if inside and not child:
            print(line.rstrip())

        if inside and child and re.search(childRe,line):
            foundChild=True
            logging.debug("Child Match: "+line.rstrip())
            print(sectionName+" ; "+line.rstrip())



    if inside and child and not foundChild:
        print(sectionName+" ; ")


if __name__ == "__main__":
    main()
