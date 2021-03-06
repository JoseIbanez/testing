#!/usr/bin/python

import re
import logging
from datetime import datetime
import kpi



class cubeCallStatCurrentDay(kpi.Cmd):
    cmdFile="call-stats-currentday.txt"
    cmdName="cubeCallStatCurrentDay"
    reIn="show sbc SBC sbe call-stats all currentday"
    reOut="#$"


    def __init__(self):
        super(cubeCallStatCurrentDay, self).__init__()
        self.currentAdj=""
        self.currentFlow=""

    def reset(self):
        super(cubeCallStatCurrentDay, self).reset()
        self.currentAdj=""
        self.currentFlow=""


    def parseLine(self,line):

        if not self.inside:
            return False

        if self.isOut(line):
            return False

        r=re.search("(?<=statistics)",line)
        if r:
            logging.debug("Reset Adjacency stat")
            self.currentAdj=None
            self.currentFlow=None


        r=re.search("(?<=statistics for the current day for source adjacency )[\w-]+",line)
        if r:
            logging.debug("Detected new Adjacency stats: (src) "+r.group(0))
            self.currentAdj=r.group(0)
            self.currentFlow="source"


        r=re.search("(?<=statistics for the current day for destination adjacency )[\w-]+",line)
        if r:
            logging.debug("Detected new Adjacency stats: (dst) "+r.group(0))
            self.currentAdj=r.group(0)
            self.currentFlow="destination"

        r=re.search("(?<=statistics for the current day for adjacency )[\w-]+",line)
        if r:
            logging.debug("Detected new Adjacency stats: (media) "+r.group(0))
            self.currentAdj=r.group(0)
            self.currentFlow="media"

        if not self.currentAdj:
  			return


        r=re.search("(?<=Total call attempts =) +(\d+)",line)
        if r:
            logging.debug(line)
            logging.debug("cubeCallAttempts: "+r.group(1))
            self.addKpi("calls","Adjacency/"+self.currentAdj+"/Direction/"+self.currentFlow,"callAttempts",int(r.group(0)))
            self.parse=True

        return True
