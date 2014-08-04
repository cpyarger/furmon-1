#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import string
import re
#
# note that this works from a linux command line:
# this is for parsing the data file
#
target="\x0f"
f = open(sys.argv[1], "rb")
line = f.readline()
L=re.split("\xfeE", line)
for item in L:
	if item.find(target) != -1:
	     # print len(item),"   ",(item[1:])
	     if 5 <= len(item)  < 6: 
			print (item[1:])
