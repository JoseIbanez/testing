#!/usr/bin/env python


import sys
import os
import string



index = 1000


for line in sys.stdin:

    src = line.strip('\n')

    dst = 'pic-{:04d}.jpg'.format(index)
    index = index + 1

    os.symlink(src, dst)
    #print src +" "+ dst



