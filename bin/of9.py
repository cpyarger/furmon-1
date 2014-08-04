#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import string
import re
#
# -*- coding: utf-8 -*-
# Mon 18 Mar 2013 02:50:39 PM EDT 
# This is the base class for the furmon object
# ref http://www.youtube.com/watch?v=CtzVNCmysFs
#
# f = open("furmon.data", "rb")
f = open(sys.argv[1], "rb")
line = f.readline()
L=re.split("\xfeE", line)
#
# goes through the current line 
class furmon:
# def __init__(self):
	def alarm(self):
		alarm="No Alarm "
		reason=" no reason "	
		target="\x00ALARM"
		for item in L:
			if item.find(target) != -1:
			     index=L.index(item)
			     alarm=(item[1:])
			     reason=L[index+1]
		return printme( alarm+reason )
	def resets(self):
		norst=""
		type="Resets"
		target="\x14"
		for item in L:
			if item.find(target) != -1:
			     # print len(item),"   ",(item[1:])
			     if 19 <= len(item)  < 22: 
					if item.find(type) != -1:
						norst=(item[1:])
		return printme( norst )
	def state(self):
		purg=""
		type="Purging"
		target="\x00"
		for item in L:
			if item.find(target) != -1:
			     # print len(item),"   ",(item[1:])
			     if 14 <= len(item)  < 25: 
					if item.find(type) != -1:
						purg=(item[1:])+"\t"
		return printme( purg )
	def systmp(self):
		# get system temprature
		temp=""
		target="B"
		for item in L:
			if item.find(target) != -1:
			     # print len(item),"   ",(item[1:])
			     if 5 <= len(item)  < 6: 
					temp="System Temp: "+(item[1:])
		return printme( temp )
	def stacktmp(self):
		# get stack temprature
		stemp=""
		target="\x0f"
		for item in L:
			if item.find(target) != -1:
			     # print len(item),"   ",(item[1:])
			     if 5 <= len(item)  < 6: 
					stemp="Stack Temp: "+(item[1:])
		return printme( stemp )
		# return printme( "flamesns Date-time" )
	def flamesns(self):
		return printme( "flame sensor?" )
	def ophours(self):
		hours=""
		type="Hours"
		target="\x14"
		for item in L:
			if item.find(target) != -1:
			     # print len(item),"   ",(item[1:])
			     if 19 <= len(item)  < 22: 
					if item.find(type) != -1:
						hours=(item[1:])
		return printme( hours )
	def thstcall(self):
		tcall=""
		target="@T"
		L=re.split("\xfeE", line)
		for item in L:
			if item.find(target) != -1:
			     tcall="Last "+(item[1:])+"-call at \t"
		return printme( tcall )
	def ignind(self):
		return printme( "Ignition-indicator Ignition-count Date-time")
	def starts(self):
		strts=""
		type="Starts"
		target="\x14"
		for item in L:
			if item.find(target) != -1:
			     # print len(item),"   ",(item[1:])
			     if 19 <= len(item)  < 22: 
					if item.find(type) != -1:
						strts=(item[1:])
		return printme( strts )
	def blower(self):
		return printme( "Blower-value Date-time")
	def button1(self):
		return printme( "Button1-pressed Date-time")
	def button2(self):
		return printme( "Button2-pressed Date-time")
#
# inserts time nearly everywhere...
def cfltime(fd):
	cflout=""
	type="Time"
	target="pf"
	#
	for item in fd:
		if item.find(target) != -1:
			if item.find(type) != -1:
				cflout=(item[3:22])
	return cflout

def printme( str ):
   '''This time stamps a  string passed into this function'''
   out=str+"\t\t"+cfltime(L)
   return out

c=furmon()
# output of objects test point
print(c.alarm())
print(c.state())
print(c.ophours())
print(c.resets())
print(c.starts())
print(c.systmp())
print(c.stacktmp())
print(c.thstcall())
print "tada"
