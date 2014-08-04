#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import string
import re
#
# Starts shown right
# note that this works from a linux command line:
# this is for parsing the data file
#
type="Time"
target="pf"
#
f = open(sys.argv[1], "rb")
line = f.readline()
L=re.split("\xfeE", line)
for item in L:
	if item.find(target) != -1:
	     # print len(item),"   ",(item[1:])
	     # if 19 <= len(item)  < 22: 
		if item.find(type) != -1:
			cfltime=(item[3:22])
# print(cfltime)
type="Purging"
target="\x00"
for item in L:
	if item.find(target) != -1:
	     # print len(item),"   ",(item[1:])
	     if 14 <= len(item)  < 25: 
			if item.find(type) != -1:
				purg=(item[1:])
print purg,"  ",cfltime
