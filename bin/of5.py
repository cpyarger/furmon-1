#!/usr/bin/python
# -*- coding: utf-8 -*-
# Mon 18 Mar 2013 02:50:39 PM EDT 
# This is the base class for the furmon object
# ref http://www.youtube.com/watch?v=CtzVNCmysFs

class furmon:
# def __init__(self):
	def alarm(self):
		return printme( "Alarm-type Date-time" )
	def state(self):
		return printme( "State-type State-counter Date-time" )
	def stacktmp(self):
		return printme( "stacktmp Date-time" )
	def flamesns(self):
		return printme( "flamesns Date-time" )
	def ophours(self):
		return printme( "Hours-operating Date-time")
	def thstcall(self):
		return printme( "Thermostat-call Date-time")
	def ignind(self):
		return printme( "Ignition-indicator Ignition-count Date-time")
	def starts(self):
		return printme( "Number-starts Date-time")
	def blower(self):
		return printme( "Blower-value Date-time")
	def button1(self):
		return printme( "Button1-pressed Date-time")
	def button2(self):
		return printme( "Button2-pressed Date-time")

def printme( str ):
   '''This prints a passed string into this function'''
   # print str
   return str



c=furmon()
# print "the alarm is",c.alarm()," and that's it"
print(c.alarm())
print(c.state())
print "tada"
