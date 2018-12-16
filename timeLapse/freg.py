#!/usr/bin/python

import re
import sys
import os
import string



index = 1


for line in sys.stdin:

    src = line.strip('\n')

    d0 =re.sub(r'.*/','./',src)

    dn = '.S01E{:02d}.'.format(index)

    dst=re.sub(r'\.\d\d\.\d\d\.\d\d\.',
           dn,
           d0)



    index = index + 1

    os.symlink(src, dst)
    print src +" -> "+ dst


