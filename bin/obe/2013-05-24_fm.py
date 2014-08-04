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
from string import digits
#
#
# establish the dreaded globals
# global L
# global inf
ver="0.20130403"
# filename="furmon.data"
filename="/home/flint/furmon/furmon.data"
#	
def intro():
	''' Prints the main story about this program and tries to warn you.'''
	print '\t %s documentation: A tale of woe and intrigue' %  os.path.basename(__file__)
	print main.__doc__
	print "for operating information type '%s -h'" % __file__

#
# This is the base class for the furmon object
# ref http://www.youtube.com/watch?v=CtzVNCmysFs
class furmon:
	hours="Hours Used" 
	tonoff="Off"
	fsensor="00"      
	fmotor="off" 
	blowsp="00"
	alarm="No Alarm"  
	reason="All is well" 
	state="Operational State"
	state_counter="0000"      
	resets="0000"       
	stack_temp="Flue Temp"
	starts="00000"       
	system_temp="System Temp"
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
def systmp(input):
	''' get system temprature '''
	temperature=""
	target="B"
	if ( str(''.join([c for c in input if input.startswith(target)]))[0:] ):  # if the element starts with the target
		temperature = cleanv(input,target)
	else: 
		temperature=""
	# return printme( temp )
	return temperature 
#
def stacktmp(input):
	''' get system temprature '''
	temperature=""
	target="F"
	if ( str(''.join([c for c in input if input.startswith(target)]))[0:] ):  # if the element starts with the target
		temperature = cleanv(input,target)
	else: 
		temperature=""
	# return printme( temp )
	return temperature 
#
def systemp(L):
	''' old system temprature '''
	temp=""
	# target="B"
	# target="\xdfF" 
	target="F"
	for item in L:
		if item.find(target) != -1:
		     # print len(item),"   ",(item[1:])
		     if 5 <= len(item)  < 7: 
				temp="System Temp: "+(item[1:4])
	# return printme( temp )
	return temp 
#
def stacktemp(L):
	'''old stack temprature'''
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
def ophours(input):
	'''This is the hours the system has been operating'''
	hours=""
	# type="Hours"
	# target="\x14"
	target="Hours"
	s=re.sub(r'[^\w]', '',input)
	# print s
	# print string.find(s, target) 
	if (string.find(s, target) == 0):
		# hours=(s[5:9])
		hours=''.join(c for c in (s[5:9]) if c in digits)
	else:
		hours=""	
	# return printme( hours )
	# return cleann(hours)
	return hours
#
#
def opstate(input):
	'''This is the state the system is operating in'''
	state=""
	target="\x00"
	# print input
	# print s
	# print string.find(s, target) 
	if (string.find(input, target) == 0):
		# state=(s[0:])
		state=re.sub(r'[^\w]', '',input[0:])
		# state=''.join(c for c in (s[5:9]) if c in digits)
	else:
		state=""	
	# return printme( state )
	# print state 
	if (state[0:4] == "Idle" ):
		state = "Idle"
	if (state[0:6] == "Firing" ):
		state = "Firing"
	if (state[0:11] == "Stabilizing" ):
		state = "Stabilizing"
	if (state[0:11] == "Shuttingdown" ):
		state = "Shuttingdown"
	if (state[0:11] == "Purging" ):
		state[0:7] != "Purging"
	# return cleann(state)
	return state
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
#					strts=(item[1:])
					return printme( strts )
#
def blower(L):
	return printme( "Blower-value Date-time")
#
def button1(L):
	return printme( "Button1-pressed Date-time")
#
def button2(L):
	return printme( "Button2-pressed Date-time")
#
def button3(L):
	return printme( "Button3-pressed Date-time")
#
def button4(L):
	return printme( "Button4-pressed Date-time")
#
#
def printme( str ):
   '''This time stamps a  string passed into this function'''
   out=str+"\t\t"+cfltime(tada)
   return out
#
def timest(L):
	'''This pulls the timestamp out of the data string'''
	type="Time"
	target="pf"
	for item in L:
		if item.find(target) != -1:
		     # print len(item),"   ",(item[1:])
		     # if 19 <= len(item)  < 22: 
				# if item.find(type) != -1:
				rawtime=float(item[9:]) # must be float to work in time machine
				# print rawtime
				# print time.localtime(rawtime)
				tm=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rawtime))
				# tm=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(1367590968.24)))
				# time=(item[8:])
	# return printme( hours )
	return tm
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
#
#
# open the information for reading
# print options.filename
# class test:
#	 filename="furmon.data"
# optioins=test
# print options.filename
def otrf():
	''' open to read file'''
	try:
		inf = open(options.filename, "rb")
	except IOError: 
		print "The file '%s' does not exist, please correct and retry..." % options.filename
		sys.exit()
	print "you opened the file from otrf"
	return inf
# 
#
def rfdl(dfile):
	''' read data line'''
	dataline=dfile.readline()
	line=re.split("\xfeE",dataline)
	# print line
	# out = open(options.filename,'a')
	return line
#
#
def dofile():
	''' loop display of data from a file '''
	# dline=otrf() # open file do this from main routine...
	print "you are in dofile routine about to read the file"
	# system_temp="System Temp"
	# frfile.stack_temp="Flue Temp"
	status="undefined"
	i = 0
	# print '%s\t\t%s' % (frfile.system_temp,frfile.stack_temp)
	# print '%i\t%s\t\t\t%s' % (i,frfile.system_temp,frfile.stack_temp)
	print '%s\t%s\t%s\t%s' % (frfile.hours,frfile.system_temp,frfile.stack_temp,frfile.state)
	#d while ( i < 8 ):
 	while True:
	 	#d i += 1 # count for run limit
		b = 1
		dataline=rfdl(dline)
		#d print dataline
		while ( b < len(dataline)):
			if ( len(dataline[b]) < 50 ):  # sets allowable element length
				l=dataline[b] 
				if systmp(l): 			#Check for a temprature in this element
					frfile.system_temp = systmp(l)
				if stacktmp(l): 		#Check for a temprature in this element
					frfile.stack_temp = stacktmp(l)
				if (ophours(l) != "" ):
					frfile.hours = ophours(l)
				else:
					frfile.hours = ""
				if (opstate(l) != "" ):
					frfile.state = opstate(l)					
					# print ophours(l) 
					#t if ( str(''.join([c for c in l if l.startswith('F')]))[0:] ):
					# if the element starts with an F
					#t frfile.stack_temp = cleanv(l,"F")
					# print '%s\t\t\t%s' % (frfile.system_temp,frfile.stack_temp)
					# print len(l),l 
					# print frfile.hours 
				# if (frfile.state != ""):
					# print "tfile outputs record = %s operatonal hours = %s" % (b,frfile.state) 
				outfile()				
	 		b += 1
#
def outfile():
	print '%s\t\t%s\t\t%s\t%s' % (frfile.hours,frfile.system_temp,frfile.stack_temp,frfile.state)
#
def outfile1():
	''' outputs a furmon object'''
	if ( frfile.hours != "" and 
		frfile.system_temp != "System Temp" and 
		frfile.stack_temp != "Flue Temp" and
		frfile.state != "Operational State"):
		print '%s\t\t%s\t\t%s\t%s' % (frfile.hours,frfile.system_temp,frfile.stack_temp,frfile.state)

def tfile():
	''' test loop display of data from a file '''
	# dline=otrf() # open file do this from main routine...
	print "using tfile to read the file"
	# system_temp="System Temp"
	# frfile.stack_temp="Flue Temp"
	status="test"
	i = 0
	# print '%s\t\t%s' % (status,status)
	print '%s\t%i\t\t\t\t%s' % (status,i,frfile.state)
	while ( i < 8 ):
 	#d while True:
	 	i += 1 # count for run limit
		b = 1
		dataline=rfdl(dline)
		#d print dataline
		while ( b < len(dataline)):
			if ( len(dataline[b]) < 50 ):  # sets allowable element length
				l=dataline[b] 
			# print "record = %s entering opstate sub" % b
			frfile.state=opstate(l)
			if ( frfile.state != "" ):
				print "leaving tfile record = %s current state = %s" % (b,frfile.state) 
	 		b += 1
#
def cleann(input):
	''' cleans up a variable returns a number no matter what'''
	# mid = re.sub(r'[^\w]', '',input)
	out = ''.join(c for c in input if c in digits)
	if out == "":
		out="0"
	return out

#
#
def cleanv(input,trigger):
	''' cleans up a variable returns a number no matter what'''
	mid = re.sub(r'[^\w]', '',(str(''.join([c for c in input if input.startswith(trigger)]))[1:4]))
	out = ''.join(c for c in mid if c in digits)
	if out == "":
		out="0"
	return out

#
def doofus():
#	# print 'Press Ctrl+C for interrupt'
#		if (len(tada) > 30):
 		if (19 <= len(tada)  < 120) :
			print 'Block %d not right with %d elements.' % (i,len(tada) )
		else:
			print tada 
			#'Block %d is and underrun with only %d elements. Press Ctrl+C to interrupt ' % (i,len(tada) )
		# print 'At %s Block %d is %d elements long. Press Ctrl+C to interrupt ' % (timest(tada),i,len(tada) )
		# print 'Block %d is %d elements long. Press Ctrl+C to interrupt ' % (i,len(tada) )
#
#		
def otrs():
	print "Using serial data from %s at %s bits per second, with a %s second time out factor" \
	% (options.serial_port, options.port_baud, options.timeout)
	serp = Serial(port=options.serial_port, baudrate=options.port_baud, timeout=6)
	print "Got past open. Press Ctrl+C to interrupt block read"
	return serp
#
def rsdl(ser):
	''' read serial data Line '''
	def signal_handler(signal, frame):
	    print " - You pressed Ctrl+C! in block read"
	    print time.time() - start_time, "seconds"
	    sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	# ser=""
	# print 'Press Ctrl+C to interrupt block read'
	while True:
	 pac_start=time.time()
	 if ser.inWaiting():
		now=str(time.time())
		dataline = ser.readline()
		outline = dataline+"\xfeEpf Time: "+now
		# print(outline)
		# out.write(outline)
		L=re.split("\xfeE", outline)
		return L
#
def doserial():
	''' loop display of raw serial data '''
	mser=otrs()
	# print 'Press Ctrl+C for interrupt'
	i = 0
	while True:
	 	i += 1
		tada=rsdl(mser)
		if (len(tada) > 30):
			print tada 
			# dfout(tada)
			# print(systmp(tada))
			# print(timest(tada))
		else:
			# print len(tada) 
			'Block %d is and underrun with only %d elements. Press Ctrl+C to interrupt ' % (i,len(tada) )
		print 'At %s Block %d is %d elements long. Press Ctrl+C to interrupt ' % (timest(tada),i,len(tada) )
#
# display 
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
	print "tada display"

#
def dcycle():
	''' display filtered output '''
	global L
	while 1:
	    L=rfdl(dline)
	    if not L:
		break
	    pass
#
def dfout(L):
	''' display filtered output '''
	# global L
	counter = 0
	while 1:
	    	# L=rfdl(dline)
		# output of objects test point
		# print c.alarm.__doc__ ," The value is",(alarm(L))
		# print c.state.__doc__ ," The value is",(state(L))
		print(alarm(L))
		print(state(L))
		print(ophours(L))
		print(resets(L))
		print(starts(L))
		print(systmp(L))
		print(stacktmp(L))
		print(thstcall(L))
		# print c.thstcall.__doc__ ," The value is",(thstcall(L))
		# print c.ignind.__doc__ ," The value is",(ignind(L)) # currently dumps L
		counter = counter + 1
		print "tada display line %s" % (counter)
		os.system('clear')
		if not L:
		    break
		pass
def main():
	''' 
	This is the main subroutine, any detail about this program belongs here.
	This program has two basic parts:
	1. data gathering from at pellergy furnace with a furmon installed and
	2. display of this data via mrtg.
Tue 02 Apr 2013 02:52:07 PM EDT this is the rewrite with the object right.
Fri 29 Mar 2013 07:02:36 AM EDT at this point the program depends on sample data
           This data is in the "New Haven Display" format and is basically binary.
Thu 04 Apr 2013 08:16:33 AM EDT new version of fm.py trying to clean up this code.
Mon 08 Apr 2013 02:17:18 PM EDT Continuing cleanup...
Fri 03 May 2013 08:46:50 AM EDT clean up serial routine
        '''
start_time = time.time()
# print "starting %s at %s " % (__file__, \
go_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
print "starting %s at %s " % (__file__, go_time)
if len(sys.argv) == 1:
	print "for operating information type '%s -h'" % __file__
	sys.exit()
#  Above handles no arguments
#
else:
# parse options and act
    	parser = optparse.OptionParser(description='Furmon Software Support Package',
                 prog=os.path.basename(__file__),
                 version='This code is version %s, and the code, %s is copyright 2013 by fits and licensed under GPLI	' % ( ver,os.path.basename(__file__) ),
                 usage= '%prog [option]')
	parser.add_option('--query', '-?', dest='bool',default=False, action='store_true',
		 help='print document string with extensive result',)
	parser.add_option('--serial', '-s', dest='serialp',default=False, action='store_true',
		 help='gather data from serial port',)
	parser.add_option("-f", "--file", dest="filename",  default="USB", 
		help="read test data from a file", metavar="FILE")
	parser.add_option("-p", "--port", dest="serial_port",  default="/dev/ttyUSB0",
		help="set serial port; default=\"/dev/ttyUSB0\"", metavar="STRING")
	parser.add_option("-b", "--baud", dest="port_baud",  default="9600",
		help="set port speed;  default=\"9600\"", metavar="STRING")
	parser.add_option("-t", "--timeout", dest="timeout",  default="6",
		help="set timeout value;  default=\"6\"", metavar="INT")
#
# Evaluates inbound arguments
	options, arguments = parser.parse_args()	# evaluate options
	if options.bool: 
		print len(sys.argv)
		intro()
		sys.exit()	
	elif options.serialp:
		print "You are at the serial routine"
		# mser=otrs()
		# print mser.__doc__rsdl(mser)
		# print dir(mser)
		#d print rsdl(mser) 
		doserial()
		sys.exit()	
	elif options.filename != "USB":
		print "You are at file routines"
		dline=otrf() # open file
		# print "this is the end of opening"
		frfile = furmon()
		print frfile.system_temp
		# print dline.__doc__
		# print dir(dline)
		# print dline.readline()
		# print re.split("\xfeE",dline.readline())
		# print inf.__doc__
		# print dir(inf)
		# print rfdl(L) # read line from file
		# print rfdl(dline) # read line from file to out
		dofile() # code to use for all object elements
		# tfile() # test individual object elements
		sys.exit()	
	elif options.serial_port != "/dev/ttyUSB0":
		print "You are at port selection"
		sys.exit()
	elif options.port_baud != "9600":
		print "You are at port selection"
		sys.exit()	
	elif options.timeout != "6":
		print "You are at timeout selection"
		sys.exit()	
# More junk
	# print 'file name %s' % options.filename
	# print 'Hello %s' % options.person


if __name__ == '__main__':
	main()
	print "that's it"


