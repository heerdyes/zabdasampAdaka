#!/usr/bin/env python3

import sys
from zabdasaGgraha import *

# ---------------- #
# global variables #
# ---------------- #

# the text buffer: a list of lines
e=Ed()

# --------- #
# main flow #
# --------- #
if len(sys.argv)==2:
  currfn=sys.argv[1]
  e.mkbuf(currfn)

e.cmdsh()
