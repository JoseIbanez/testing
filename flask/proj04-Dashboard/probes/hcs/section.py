#!/usr/bin/python
import sys
import re
import logging
import argparse

class Section:
    """Parse show run cisco config to get sections, or configuration pieces"""
    i = 12345

    def __init__(self,section,child):
        self.deep=""
        self.inside=False
        self.sectionName=""
        self.foundChild=False
        self.child=child

        self.beginRe = re.compile(section)
        self.insideRe = re.compile("")
        self.childRe = re.compile(child)

    def parse(self,line):

        if (self.inside and not re.match(self.insideRe,line)):
            logging.debug("Exit match")
            logging.debug(line.rstrip())
            self.inside=False

            if self.child and not self.foundChild:
                print(self.sectionName+" ; ")



        if ( not self.inside and re.search(self.beginRe,line.lstrip())):
            self.inside=True
            deepn=len(line)-len(line.lstrip())
            self.deep=" "* (deepn+1)
            self.sectionName=line.rstrip()
            self.foundChild=False
            self.insideRe = re.compile(self.deep)
            logging.debug("Match, deep:"+str(deepn)+" >"+self.deep+"<")


        if self.inside and not self.child:
            print(line.rstrip())

        if self.inside and self.child and re.search(self.childRe,line):
            self.foundChild=True
            logging.debug("Child Match: "+line.rstrip())
            print(self.sectionName+" ; "+line.rstrip())

        return self.inside

    def close(self):
        if self.inside and self.child and not self.foundChild:
            print(self.sectionName+" ; ")

    def __exit__(self, *err):
        self.close()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--section",  metavar="STRING", help="String to match in section header", default="")
    parser.add_argument("-c", "--child", metavar="STRING", help="String to match inside section", default="")
    parser.add_argument("--debug", nargs='?', help="Enable debug", default="")
    args = parser.parse_args()

    if (args.debug is None):
        logging.basicConfig(level=logging.DEBUG)

    logging.debug("Parameter section:"+args.section)
    name=args.section

    logging.debug("Parameter child:"+args.child)
    child=args.child


    section=Section(name,child)

    for line in sys.stdin:
        section.parse(line)


    section.close()


if __name__ == "__main__":
    main()
