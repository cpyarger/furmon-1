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
target="@T"
f = open(sys.argv[1], "rb")
line = f.readline()
# re.split("\xfeE", line)
L=re.split("\xfeE", line)
# re.split("\xfeE\x00", line)
for item in L:
#	if item.find(sys.argv[2]) != -1:
	if item.find(target) != -1:
	     print(item[1:])

