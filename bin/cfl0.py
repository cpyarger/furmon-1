#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import string
import re
# import MySQLdb
#
# note that this works from a linux command line:
# this is for parsing the data file
#
target="\x0f"
f = open(sys.argv[1], "rb")
line = f.readline()
# re.split("\xfeE", line)
L=re.split("\xfeE", line)
# re.split("\xfeE\x00", line)
print L
