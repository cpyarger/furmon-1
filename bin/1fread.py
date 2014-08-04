#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os
import re
import serial
import io
import csv
import sys
import MySQLdb
from subprocess import call

# Connect to Mysql DB


portread = os.system("dmesg |grep ttyUSB |tail -n 1|cut -d : -f3")

# Open connection to the arduino, 
port = "/dev/ttyUSB" + str(portread)
 #now = datetime.datetime.now()
ser = serial.Serial(port, 9600, timeout=5) 

#open connection to the arduino
#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))  # clear buffering get the data out *now*
#sio.flush()
time.sleep(.75) # Give the buffer time to clear      
#line3  = ser.readline()
clearline = ser.readline()   # read a '\n' terminated line1 usually the one line with misformatted text
dataline = ser.readline()   # read a '\n' terminated line4
ser.close() 
# print (line1), ('line1')
# print (clearline)
# print (clearline.strip())
rx = re.compile('\W+')
res = rx.sub(' ', clearline).strip()
rx = re.compile('\W+')
res = rx.sub(' ', dataline).strip()
# print (dataline)

# print (os.system("dmesg |grep ttyACM |tail -n 1|cut -d : -f3"))
filewrite = open("test.cap", "rw+")
line = filewrite.write( dataline )
line2 = filewrite.write( clearline )

filewrite.close()


strings = os.system("strings test.cap > strings.a")
temp = os.system("")
fileread = open ("strings.a", "r")

fileread.close()

temp = os.system("cat strings.a |grep EF |cut -c 3- > temp ")
starts = os.system("cat strings.a |grep Starts  > starts ")
idle = os.system("cat strings.a |grep Idle  > Idle ")
hours = os.system("cat strings.a |grep Hours > Hours")
reets = os.system("cat strings.a |grep Resets  > resets ")
print "done"
