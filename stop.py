#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from config.config import *

f = open(PROGRAM_ROOT + os.sep + "sys.pid", "r")
pid = int(f.readline())
cmd = "kill %d" % pid
os.system(cmd)