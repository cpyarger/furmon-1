#!/usr/bin/env python
import os
import re
import sys
import optparse
import subprocess
import signal
import time
import serial
import io
import csv
import string
from subprocess import call
from serial import Serial
#
class furmon:
# def __init__(self):
	def alarm(self):
		'''This determines if there is an alarm, this also reports the reason '''
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
		'''This is the number of resets '''
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
#
	def state(self):
		'''This is the purging state.'''
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
#
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
#
	def stacktmp(self):
		'''this gets the stack temprature'''
		stemp=""
		target="\x0f"
		for item in L:
			if item.find(target) != -1:
			     # print len(item),"   ",(item[1:])
			     if 5 <= len(item)  < 6: 
					stemp="Stack Temp: "+(item[1:])
		return printme( stemp )
		# return printme( "flamesns Date-time" )
#
	def flamesns(self):
		''' Is the sensor sensing flame?'''
		return printme( "flame sensor?" )
#
	def ophours(self):
		'''This is the hours the system has been operating'''
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
#
	def thstcall(self):
		'''This is the thermostat call, it is either on or off.'''
		tcall=""
		target="@T"
		# L=re.split("\xfeE", dataline)
		for item in L:
			if item.find(target) != -1:
			     tcall="Last "+(item[1:])+"-call at \t"
		return printme( tcall )
#
	def ignind(self):
		'''Ignition-indicator Ignition-count Date-time'''
		print "input string is %s" % L
		return printme( "Ignition-indicator Ignition-count Date-time")
#
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
#
def FileCheck(fn):
    try:
      open(fn, "r")
      return 1
    except IOError:
      print "Error: File does not appear to exist."
      return 0
#
# reference
# http://www.alexonlinux.com/pythons-optparse-for-human-beings

def main():
	''' 
	This is the main subroutine, any detail about this program belongs here.
	This program has two basic parts:
	1. data gathering from at pellergy furnace with a furmon installed and
	2. display of this data via mrtg.
        '''
#
# establish the globals
	global L
	inf=""
	# L="banana"  # is this global now?
	ver="0.20130328"
#
# parse options and act
	# print 'Hello %s' % options.person
	# print 'file name %s' % options.filename
    	parser = optparse.OptionParser(description='Furmon Software Support Package',
                 prog=os.path.basename(__file__),
                 version='This is version %s. This code, %s is copyright 2013 by fits and licensed under GPLI	' % ( ver,os.path.basename(__file__) ),
                 usage= '%prog [option]')
	parser.add_option('--query', '-?', dest='bool',default=False, action='store_true',
		 help='print document string with extensive result',)
	# parser.add_option('--functs', '-s', help='starts operational functions', dest='function',  action='store')
	parser.add_option('--person', '-p', dest="person", default="world")
	parser.add_option('-n', '--new', help='creates a new object')
	parser.add_option("-f", "--file", dest="filename",  default="file", help="read test data from a file", metavar="FILE")
	# parser.add_option("-s", "--serial", dest="filename",  default="file",
#
	options, arguments = parser.parse_args()	# evaluate options
	if options.bool: 
		print '%s documentation' %  os.path.basename(__file__)
		print main.__doc__
		print "for operating information type '%s -h'" % __file__
		sys.exit()	
#
# open the information for reading
if filename:
	try:
		inf = open(options.filename, "rb")
	except IOError: 
		print "The file does not exist, exiting gracefully"
		sys.exit()	
#
# read data line
	dataline=inf.readline()
	L=re.split("\xfeE",dataline)
	# print L
	# out = open(options.filename,'a')
# display 
	c=furmon()
	# output of objects test point
	# print c.alarm.__doc__ ," The value is",(c.alarm())
	# print c.state.__doc__ ," The value is",(c.state())
	print(c.alarm())
	print(c.state())
	print(c.ophours())
	print(c.resets())
	print(c.starts())
	print(c.systmp())
	print(c.stacktmp())
	print(c.thstcall())
	# print c.thstcall.__doc__ ," The value is",(c.thstcall())
	# print c.ignind.__doc__ ," The value is",(c.ignind()) # currently dumps L
	print "tada"

if __name__ == '__main__':
	print "starting %s" % __file__
	if len(sys.argv) == 1:
		print "for operating information type '%s -h'" % __file__
		sys.exit()
	main()
	print "that's it"


