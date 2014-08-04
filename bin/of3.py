#!/usr/bin/python
# -*- coding: utf-8 -*-
# Mon 18 Mar 2013 02:50:39 PM EDT 
# This is the base class for the furmon object
# ref http://www.youtube.com/watch?v=CtzVNCmysFs

class furmon:
	def alarm(self):
		print "Alarm-type Date-time"
	def state(self):
		print "State-type State-counter Date-time"
	def stacktmp(self):
		print "stacktmp Date-time"
	def flamesns(self):
		print "flamesns Date-time"
	def ophours(self):
		print "Hours-operating Date-time"
	def thstcall(self):
		print "Thermostat-call Date-time"
	def ignind(self):
		print "Ignition-indicator Ignition-count Date-time"
	def alarm(self):
		print "ding ding Date-time"
	def starts(self):
		print "Number-starts Date-time"
	def blower(self):
		print "Blower-value Date-time"
	def button1(self):
		print "Button1-pressed Date-time"
	def button2(self):
		print "Button2-pressed Date-time"

def printme ( str ):
   "This prints a passed string into this function"
   print str
   return


