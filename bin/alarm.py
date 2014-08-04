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
#
cfltime="TBA"
for item in L:
	if item.find(target) != -1:
	     # print len(item),"   ",(item[1:])
	     # if 19 <= len(item)  < 22: 
		if item.find(type) != -1:
			# cfltime=(item[3:22])
			clftime="TBA"
# print(cfltime)
type="ALARM"
# target="\x00"
target="\x00ALARM"
alarm=""	
for item in L:
	if item.find(target) != -1:
	     index=L.index(item)
	     print(item[1:])
	     print L[index+1]
	     # print len(item),"   ",(item[1:])
	     # if 19 <= len(item)  < 22: 
			if item.find(type) != -1:
				# print L.index(item)
				
# print(alarm)
				# alarm="ding ding"
print alarm,"  ",cfltime
