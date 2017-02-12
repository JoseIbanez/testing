#!/usr/bin/python

import re
import logging
from datetime import datetime
import kpi

class cubeCallStatCurrentDay(kpi.Kpi):
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
            self.currentFlow="src"

        r=re.search("(?<=statistics for the current day for destination adjacency )[\w-]+",line)
        if r:
            logging.debug("Detected new Adjacency stats: (dst) "+r.group(0))
            self.currentAdj=r.group(0)
            self.currentFlow="dst"

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
            self.kpi[self.currentAdj+'/'+self.currentFlow+':cubeCallAttemps']=int(r.group(0))
            #self.currentAdj=r.group(0)
            #self.currentFlow="media"
 



        return True


