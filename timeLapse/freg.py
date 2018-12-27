#!/usr/bin/python

import re
import sys
import os
import string




src = sys.argv[1]

srcDir = os.path.dirname(src)
filename = os.path.basename(src)
print "filename", filename


z = re.search("\.(\d\d)\.(\d\d)\.(\d\d)\.", filename)
#z = re.match("(\d\d)", filename)


print z.groups()

cap = None

if z:
    #print z.groups()[0]
    #print z.groups()[1]
    #print z.groups()[2]
    cap = ".S%sE%s%s." % ( z.groups()[0], z.groups()[1], z.groups()[2] )
    print cap


if cap:
   dst = re.sub(r'\.\d\d\.\d\d\.\d\d\.',cap, filename)
else:
   dst = filename



os.symlink(src, dst)
print src +" -> "+ dst


