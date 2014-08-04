#!/bin/bash
# pflint Thu 13 Jun 2013 07:20:23 AM EDT 
#
# kills fm.py
ps aux       	 | # look through the list
 grep fm.py  	 | # find the program
 grep sample 	 | # filter for data file
 tail -1     	 | # take last choice displayed	 
 tr -s [:space:] | # make it so you can filter the line
 cut -d " " -f 2 | # get the process id
xargs kill -9      # kill it.
