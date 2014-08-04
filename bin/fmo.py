#!/usr/bin/env python
#
# pflint Mon 01 Apr 2013 07:29:56 AM EDT have methods evaluate attributes
# once all the attributes are evaluated then reaport...
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
# Tue 02 Apr 2013 02:25:47 PM EDT  
# This is the base class for the furmon object
# ref http://www.youtube.com/watch?v=CtzVNCmysFs
class furmon:
	hours="0000" 
	tonoff="Off"
	fsensor="00"      
	fmotor="off" 
	blowsp="00"
	alarm="No Alarm"  
	reason="All is well" 
	state="Purging"
	state_counter="0000"      
	resets="0000"       
	stack_temp="000"
	starts="00000"       
	system_temp="000"
	butn1="Param"
	butn2="Test"
	butn3="Enabl"
	butn4="Feed"
# The goal of this program is to fill in as many attributes of the object as you can.
# These are the basic functions
#
# Here are the tests
def alarm(L):
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
#

def resets(L):
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

def state(L):
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

def systmp(L):
	''' get system temprature '''
	temp=""
	# target="B"
	# target="\xdfF" 
	target="F"
	for item in L:
		if item.find(target) != -1:
		     # print len(item),"   ",(item[1:])
		     if 5 <= len(item)  < 7: 
				temp="System Temp: "+(item[1:4])
	return printme( temp )
#

def stacktmp(L):
	'''this gets the stack temprature'''
	stemp=""
	target="\x0f"
	for item in L:
		if item.find(target) != -1:
		     # print len(item),"   ",(item[1:])
		     if 5 <= len(item)  < 7: 
				stemp="Stack Temp: "+(item[1:4])
	return printme( stemp )
	# return printme( "flamesns Date-time" )
#

def flamesns(L):
	''' Is the sensor sensing flame?'''
	return printme( "flame sensor?" )
#

def ophours(L):
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

def thstcall(L):
	'''This is the thermostat call, it is either on or off.'''
	tcall=""
	target="@T"
	# L=re.split("\xfeE", dataline)
	for item in L:
		if item.find(target) != -1:
		     tcall="Last "+(item[1:])+"-call at \t"
	return printme( tcall )
#

def ignind(L):
	'''Ignition-indicator Ignition-count Date-time'''
	print "input string is %s" % L
	return printme( "Ignition-indicator Ignition-count Date-time")
#

def starts(L):
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

def blower(L):
	return printme( "Blower-value Date-time")

def button1(L):
	return printme( "Button1-pressed Date-time")

def button2(L):
	return printme( "Button2-pressed Date-time")

def button3(L):
	return printme( "Button3-pressed Date-time")

def button4(L):
	return printme( "Button4-pressed Date-time")
#
# inserts time nearly everywhere...
def cfltime(fd):
	'''inserts time nearly everywhere...'''
	cflout=""
	type="Time"
	target="pf"
	#
	for item in fd:
		if item.find(target) != -1:
			if item.find(type) != -1:
				rawtime=float(item[9:21]) # must be float to work in time machine
				cflout=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rawtime))
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
    ''' Not using this routine yet'''
    try:
      open(fn, "r")
      return 1
    except IOError:
      print "Error: File does not appear to exist."
      return 0
#
# reference
# http://www.alexonlinux.com/pythons-optparse-for-human-beings

