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
from subprocess import call
from serial import Serial
#
version="20130322"
# note that this works from a linux command line:
# device="/dev/ttyUSB0";miniterm.py -p $device |strings -n12
# Connect to Mysql DB
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
def main():
	out = open('furmon.data','a')
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
		# outline = now+"\xfeE"+dataline
		outline = dataline+"\xfeEpf Time: "+now
		# print(outline)
		out.write(outline)
		print 'At %d, after %d seconds the length of the data is: %d' % ( time.time(), ( time.time() - pac_start ), len(dataline))
		# print 'At %(now)d, after %(done)d seconds the length of the data is: %(length)d' % ('now':time.time(), 'done':( time.time() - pac_start ), 'lentgh':len(dataline))
		# print 'At %(time.time())d, after %( time.time() - pac_start )d seconds the length of the data is:',len(dataline)
		# print 'After %d seconds the length of the data is:' % ( time.time() - pac_start ), len(dataline)
	#
#

"""
Junk
#now = datetime.datetime.now()
# ser = serial.Serial(port, 9600, timeout=5) 
#open connection to the arduino
#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))  # clear buffering get the data out *now*
#sio.flush()
#t time.sleep(.75) # Give the buffer time to clear      
#line3  = ser.readline()
#t clearline = ser.readline()   # read a '\n' terminated line1 usually the one line with misformatted text
# dataline = ser.readline()   # read a '\n' terminated line4
# print (line1), ('line1')
# print (clearline)
# print (dataline)
#

if __name__ == "__main__":
	    main()
"""
start_time = time.time()
main()
ser.close() 
out.close()
print time.time() - start_time, "seconds"

