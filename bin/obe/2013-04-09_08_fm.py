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
#
# establish the dreaded globals
# global L
# global inf
ver="0.20130329"
# filename="furmon.data"
filename="/home/flint/furmon/furmon.data"

def intro():
	''' Prints the main story about this program and tries to warn you.'''
	print '\t %s documentation: A tale of woe and intrigue' %  os.path.basename(__file__)
	print main.__doc__
	print "for operating information type '%s -h'" % __file__

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
def otrs():
	print "Using serial data from %s at %s bits per second, with a %s second time out factor" \
	% (options.serial_port, options.port_baud, options.timeout)
	serp = Serial(port=options.serial_port, baudrate=options.port_baud, timeout=6)
	print "Got past open"
	return serp
#
def rsdl(ser):
	''' read serial data Line '''
	def signal_handler(signal, frame):
	    print " - You pressed Ctrl+C! "
	    print time.time() - start_time, "seconds"
	    sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	# ser=""
	print 'Press Ctrl+C for interrupt'
	while True:
	 pac_start=time.time()
	 if ser.inWaiting():
		now=str(time.time())
		dataline = ser.readline()
		outline = dataline+"\xfeEpf Time: "+now
		# print(outline)
		# out.write(outline)
		L=re.split("\xfeE", dataline)
		return L
#
def getL():
	done_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	print 'At %s, after %d seconds the length of the data is: %d' \
	% ( done_time, ( time.time() - pac_start ), len(dataline))
	# print 'At %(now)d, after %(done)d seconds the length of the data is: %(length)d' % ('now':time.time(), 'done':( time.time() - pac_start ), 'lentgh':len(dataline))
	# print 'At %(time.time())d, after %( time.time() - pac_start )d seconds the length of the data is:',len(dataline)
	# print 'After %d seconds the length of the data is:' % ( time.time() - pac_start ), len(dataline)
	#
	# sys.exit()
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
#
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
	print "tada display"


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
		print "You are at serial routines"
		mser=otrs()
		# print mser.__doc__
		# print dir(mser)
		print rsdl(mser) # NameError: global name 'ser' is not defined
		sys.exit()	
	elif options.filename != "USB":
		print "You are at file routines"
		dline=otrf() # open file
		print "you opened the file"
		# print dline.__doc__
		# print dir(dline)
		# print dline.readline()
		# print re.split("\xfeE",dline.readline())
		# print inf.__doc__
		# print dir(inf)
		# print rfdl() # read line from file
		print rfdl(dline) # read line from file
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


