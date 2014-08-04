#!/usr/bin/python
# -*- coding: utf-8 -*-
import signal
import time
import os
import re
import serial
import io
import csv
import sys
import string
from subprocess import call
from serial import Serial
#
version="20130322"
# note that this works from a linux command line:
# device="/dev/ttyUSB0";miniterm.py -p $device |strings -n12
#
# -*- coding: utf-8 -*-
# Mon 18 Mar 2013 02:50:39 PM EDT 
# This is the base class for the furmon object
# ref http://www.youtube.com/watch?v=CtzVNCmysFs
#

# f = open("furmon.data", "rb")
# f = open(sys.argv[1], "rb")
# line = f.readline()
# L=re.split("\xfeE", line)
L=""
# def splitsvl(f)
#	L=re.split("\xfeE", line)
#	return 
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
		# L=re.split("\xfeE", dataline)
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

#
FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def dump(src, length=8):
    N=0; result=''
    while src:
       s,src = src[:length],src[length:]
       hexa = ' '.join(["%02X"%ord(x) for x in s])
       s = s.translate(FILTER)
       result += "%04X   %-*s   %s\n" % (N, length*3, hexa, s)
       N+=length
    return result



"""
# this is an example which works if you uncomment this block
s=("This 10 line function is just a sample of pyhton power "
   "for string manipulations.\n"
   "The code is \x07even\x08 quite readable!")

print dump(s)
"""
#

# portread = os.system("dmesg |grep ttyACM |tail -n 1|cut -d : -f3")
# Open connection to the arduino, 
# port = "/dev/ttyUSB0" + str(portread)
def getdata():
	# out = open('furmon.data','a')
	port = "/dev/ttyUSB0"
	# ser = Serial(port="/dev/ttyUSB0", baudrate=9600 ) # set the parameters to what you want
	ser = Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=6) # set the parameters to what you want 5 is good as well
	# dataline="the quick brown fox" # sample data
	def signal_handler(signal, frame):
	    print " - You pressed Ctrl+C! "
	    print time.time() - start_time, "seconds"
	    sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	print 'Press Ctrl+C for interrupt'
	while True:
	 pac_start=time.time()
	 if ser.inWaiting():
		now=str(time.time())
		dataline = ser.readline()
		outline = dataline+"\xfeEpf Time: "+now
		if len(dataline) > 10: 
			outobjs(outline)
			print(outline)
		# out.write(outline)
		print 'At %d, after %d seconds the length of the data is: %d' % ( time.time(), ( time.time() - pac_start ), len(dataline))
		# print 'At %(now)d, after %(done)d seconds the length of the data is: %(length)d' % ('now':time.time(), 'done':( time.time() - pac_start ), 'lentgh':len(dataline))
		# print 'At %(time.time())d, after %( time.time() - pac_start )d seconds the length of the data is:',len(dataline)
		# print 'After %d seconds the length of the data is:' % ( time.time() - pac_start ), len(dataline)
	#
#
def outobjs(I):
	# output of objects test point
	L=re.split("\xfeE", I)
	c=furmon()
	print L
	print(c.alarm())
	print(c.state())
	print(c.ophours())
	print(c.resets())
	print(c.starts())
	print(c.systmp())
	print(c.stacktmp())
	print(c.thstcall())
	print "tada"

"""
if __name__ == "__main__":
	    main()
"""
start_time = time.time()
main()
ser.close() 
out.close()
print time.time() - start_time, "seconds"

