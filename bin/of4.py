#!/usr/bin/python
# -*- coding: utf-8 -*-
# Mon 18 Mar 2013 02:50:39 PM EDT 
# This is the base class for the furmon object
# ref http://www.youtube.com/watch?v=CtzVNCmysFs

class furmon:
# def __init__(self):
	def alarm(self):
		printme( "Alarm-type Date-time")
	def state(self):
		printme( "State-type State-counter Date-time")
	def stacktmp(self):
		printme( "stacktmp Date-time")
	def flamesns(self):
		printme( "flamesns Date-time")
	def ophours(self):
		printme( "Hours-operating Date-time")
	def thstcall(self):
		printme( "Thermostat-call Date-time")
	def ignind(self):
		printme( "Ignition-indicator Ignition-count Date-time")
	def starts(self):
		printme( "Number-starts Date-time")
	def blower(self):
		printme( "Blower-value Date-time")
	def button1(self):
		printme( "Button1-pressed Date-time")
	def button2(self):
		printme( "Button2-pressed Date-time")

def printme( str ):
   "This prints a passed string into this function"
   print str 
   return


