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
	    def __init__(self):
		self.thstcall="Call"
		self.recno="#"
		self.hours="Hours Used" 
		self.tonoff="Off"
		self.fsensor="00"      
		self.fmotor="off" 
		self.blowsp="00"
		self.alarm="No Alarm"  
		self.reason="All is well" 
		self.opstate="Operational State"
		self.state_counter="0000"      
		self.resets="0000"       
		self.stack_temp="Flue Temp"
		self.starts="000"       
		self.system_temp="System Temp"
		self.butn1="Param"
		self.butn2="Test"
		self.butn3="Enabl"
		self.butn4="Feed"
# The goal of this program is to fill in as many attributes of the object as you can.
# These are the basic methods
	#d def expose(self):
	# ''' prints all the attributes of this object '''
	# note this is an example from 
	# http://www.saltycrane.com/blog/2008/09/how-iterate-over-instance-objects-data-attributes-python/
	#d for attr, value in a.__dict__.iteritems():  
        #d     print attr, value

#
# exposes attributes and values in an object
def expose(obj):
	''' prints all the attributes of this object '''
	# note this is based on an example from 
	# http://www.saltycrane.com/blog/2008/09/how-iterate-over-instance-objects-data-attributes-python/
	#d a=obj()
	for attr, value in obj.__dict__.iteritems():  
	  if len(attr) >=8:
            print '%s\t%s' % (attr, value)
	  else:
            print '%s\t\t%s' % (attr, value)
            # print '%d\t%s\t\t%s' % (len(attr),attr, value)

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
def resets(input):
	'''This is the number of resets '''
	norst=""
	target="Resets:"
	# type="Resets:"
	# target="\x14"
	s=re.sub(r'[^\w]', '',input)
	if (string.find(input, target) > 0):
		# print "Got One in"
		# print s
		beg=(string.find(s, target)+len(target))
		# print beg
		resets=s[(beg):(beg+5)]
		# print "new resets =", resets
		# resets=''.join(c for c in (s[5:9]) if c in digits)
	# print "length of resets",len(resets)
	# print "length of frfile.resets",len(frfile.resets)
	if (len(resets) > len(frfile.resets)) or (cleann(resets) > frfile.resets):
		frfile.resets=cleann(resets)
		return cleann(resets)
		# return frfile.resets
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
		# print "got a good temp"
	else: 
		temperature=frfile.system_temp
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
		temperature=frfile.stack_temp
	# return printme( temp )
	return temperature 
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
	if len(cleann(frfile.hours)) >= len(cleann(hours)) :
		hours=frfile.hours
		# hours=""	
	# return printme( hours )
	return cleann(hours)
	# return hours
#
#
def opstate(input):
	'''This is the state the system is operating in'''
	# http://www.pythonforbeginners.com/strings/
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
		state=frfile.opstate	
	# return printme( state )
	# print state 
	x=0
	statepairs = [ 	('IDL','idle') , 
			('I','idle') , 
			('IGN','igniting') , 
			('FEE','feedstart'),
			('FIR','firing'),
			('STA','stabilizing'),
			('SH','shuttingdown'), 	# test for comments in line...
			('S','shuttingdown'),	# this appears to work.
			('PU','purging'),
			('ALA','alarm') ]
	for s in statepairs:
		tart=len(statepairs[x][0])
		if (state.upper()[0:tart] == statepairs[x][0] ):
			state = statepairs[x][1]
		x += 1
	# return cleann(state)
	if (state.isupper() or state.isdigit()):
		state = frfile.opstate
	return state
#
def thstcall(input):
	'''This is the thermostat call, it is either on or off.'''
	tcall=""
	target="@T"
	# L=re.split("\xfeE", dataline)
	if (string.find(input, target) == 0):
		# state=(s[0:])
		state=re.sub(r'[^\w]', '',input[0:])
		# state=''.join(c for c in (s[5:9]) if c in digits)
	else:
		state=""	
	return state[0:1]
#
def ignind(L):
	'''Ignition-indicator Ignition-count Date-time'''
	print "input string is %s" % L
	return printme( "Ignition-indicator Ignition-count Date-time")
#
def starts(input):
	# print "entering starts function"
	starts=""
	beg=0
	target="Starts:"
	s=re.sub(r'[^\w]', '',input)
	if (string.find(input, target) > 0):
		# print "Got One in"
		# print s
		beg=(string.find(s, target)+len(target))
		# print beg
		starts=s[(beg):(beg+5)]
		# print "new starts =", starts
		# starts=''.join(c for c in (s[5:9]) if c in digits)
	# print "length of starts",len(starts)
	# print "length of frfile.starts",len(frfile.starts)
	if (len(starts) > len(frfile.starts)) or (cleann(starts) > frfile.starts):
		frfile.starts=cleann(starts)
		return cleann(starts)
		# return frfile.starts
#
def old_starts():
	for item in input:
		if item.find(target) != -1:
		     # print len(item),"   ",(item[1:])
		     if 19 <= len(item)  < 22: 
				if item.find(type) != -1:
					# strts=(item[1:])
					# return printme( strts )
					return strts  
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
def cleann(thing):
	''' cleans up a variable returns a number no matter what'''
	# mid = re.sub(r'[^\w]', '',thing)
	out = ''.join(c for c in thing if c in digits)
	if out == "":
		out="0"
	return out

#
#
def cleanv(thing,trigger):
	''' cleans up a variable returns a number no matter what'''
	mid = re.sub(r'[^\w]', '',(str(''.join([c for c in thing if thing.startswith(trigger)]))[1:4]))
	out = ''.join(c for c in mid if c in digits)
	if out == "":
		out="0"
	return out

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
#
def rfdl(dfile):
	''' read data line'''
	dataline=dfile.readline()
	line=re.split("\xfeE",dataline)
	# print line
	# out = open(options.filename,'a')
	if dataline == '': 
	 dataline = "EOF"
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
	#d while ( i < 8 ):
 	while True:
	 	# while ( len(rfdl(dline)) != 0):
		# 	if (rfdl(dline) == "EOF"):
		#		break
	 	# while rfdl(dline):
	 	i += 1 # count for run limit
		b = 1
		dataline=rfdl(dline)
		#d print dataline
		while ( b < len(dataline)):
			os.system('clear')
			if ( len(dataline[b]) < 50 ):  # sets allowable element length
				l=dataline[b] 
				frfile.system_temp = systmp(l)
				# print systmp(l)
				starts(l)
				frfile.stack_temp = stacktmp(l)
				frfile.hours = ophours(l)
				frfile.opstate = opstate(l)					
				frfile.thstcall = thstcall(l)					
				frfile.resets = resets(l)				
				frfile.recno = i
				# outfile1()				
				# outfile()				
				print 'in line %d' % (b)
				expose(frfile)
				os.system('sleep 0.25s')
				# os.system('clear')
	 		b += 1
#
def tfile():
	''' test loop display of data from a file '''
	# dline=otrf() # open file do this from main routine...
	print "using tfile to read the file"
	# system_temp="System Temp"
	# frfile.stack_temp="Flue Temp"
	status="test"
	i = 0
	# print '%s\t%i\t\t\t\t%s' % (status,i,frfile.opstate)
	#t while ( i < 8 ):
 	while True:
	 	#t i += 1 # count for run limit
		b = 1
		dataline=rfdl(dline)
		#d print dataline
		while ( b < len(dataline)):
			if ( len(dataline[b]) < 50 ):  # sets allowable element length
				l=dataline[b] 
			# print "record = %s frfile.starts = %s" % b,frfile.starts
			# print "length of l =",len(l)
			# frfile.starts=starts(l)
			# print "starts = ",starts(l)
			print resets(l)
			print "frfile.resets = ",frfile.resets
			# print "record = %s entering opstate sub" % b
			# print "leaving tfile record = %s current state = %s" % (b,frfile.starts) 
	 		b += 1
#
#
def Sfile():
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
Tue 11 Jun 2013 01:48:23 PM EDT working on the file based system
        '''
start_time = time.time()
# frfile = furmon() # instantiate the furmon class to frfile
# print "starting %s at %s " % (__file__, \
go_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
print "starting %s at %s " % (__file__, go_time)
if len(sys.argv) == 1:
	print "Welcome to fm.py. For operating information type '%s -h'" % __file__
	sys.exit()
#  Above handles no arguments
#
else:
# parse options and act
    	parser = optparse.OptionParser(description='Furmon Software Support Package',
                 prog=os.path.basename(__file__),
                 version='This code is version %s, and the code, %s is copyright 2013 by fits and licensed under GPLI	' % ( ver,os.path.basename(__file__) ),
                 usage= '%prog [option]')
   	#
	parser.add_option('-?', '--query',   dest='bool',default=False, action='store_true',help='print document string with extensive result',)
	parser.add_option('-s', '--serial',  dest='serialp',default=False, action='store_true',help='gather data from serial port',)
	parser.add_option("-f", "--file",    dest="filename",  default="USB",help="read test data from a file", metavar="FILE")
	parser.add_option("-p", "--port",    dest="serial_port",  default="/dev/ttyUSB0",help="set serial port; \tdefault=\"/dev/ttyUSB0\"", metavar="STRING")
	parser.add_option("-b", "--baud",    dest="port_baud",  default="9600",help="set port speed;  \tdefault=\"9600\"", metavar="STRING")
	parser.add_option("-t", "--timeout", dest="timeout",  default="6",help="set timeout value;  \tdefault=\"6\"", metavar="INT")
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
		print "this is the end of opening"
		frfile = furmon() # instantiate the furmon class to frfile
		# print frfile.system_temp
		# print dline.__doc__
		# print dir(dline)
		# print dline.readline()
		# print re.split("\xfeE",dline.readline())
		# print inf.__doc__
		# print dir(inf)
		# print rfdl(L) # read line from file
		# print rfdl(dline) # read line from file to out
		# print rfdl(dline) # read line from file to out
		# dofile() # code to use for all object elements
		tfile() # test individual object elements
		# expose(furmon)
		# expose(frfile)
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


