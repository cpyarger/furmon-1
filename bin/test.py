#!/usr/bin/env python
import os
import optparse
import subprocess
# reference
# http://www.alexonlinux.com/pythons-optparse-for-human-beings

def main():
	''' 
	This is the main subroutine, any detail about this program belongs here.
	This program has two basic parts:
	1. data gathering from at pellergy furnace with a furmon installed and
	2. display of this data via mrtg.
        '''
	ver="0.2"
    	parser = optparse.OptionParser(description='Furmon Software Support Package',
                 prog=os.path.basename(__file__),
                 version='This is %s. It is fits version %s and is copyright 2013 by fits and licensed under GPLI	' % ( os.path.basename(__file__),ver ),
                 usage= '%prog [option]')
	parser.add_option('-b', help='print document string', dest='bool',default=False, action='store_true')
	parser.add_option('-s', help='arguments', dest='opt_args',  action='store')
	parser.add_option('--person', '-p', default="world")
	parser.add_option('--query', '-?', default="banana", dest='query',  action='store')
	parser.add_option('-n', '--new', help='creates a new object')
	parser.add_option("-f", "--file", dest="filename",  default="file",
                  help="write report to FILE", metavar="FILE")
	options, arguments = parser.parse_args()
	print 'Hello %s' % options.person
	# print 'Fruit flies like %s' % options.query
	print 'opt_args %s' % options.opt_args
	# print 'file name %s' % options.filename
	if options.bool: 
		print '%s documentation' %  os.path.basename(__file__)
		print main.__doc__
		print "for operating information type '%s -h'" % __file__

if __name__ == '__main__':
	print "starting"
	main()
	print "that's it"


