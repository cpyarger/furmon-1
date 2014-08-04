#!/usr/bin/env python
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
	if len(sys.argv) == 1:
		print "for operating information type '%s -h'" % __file__
	print 
    	parser = optparse.OptionParser(description='A unix testbox',
                 prog='ibmfr1.py',
                 version='fits 0.1',
                 usage= '%prog [option]')
	parser.add_option('-s', help='arguments', dest='opt_args',  action='store')
	parser.add_option('--person', '-p', default="world")
	parser.add_option('--query', '-?', default="banana", dest='query',  action='store')
	parser.add_option('-b', help='boolean option', dest='bool',default=False, action='store_true')
	parser.add_option('-n', '--new', help='creates a new object')
	parser.add_option("-f", "--file", dest="filename",  default="file",
                  help="write report to FILE", metavar="FILE")
	options, arguments = parser.parse_args()
	print 'Hello %s' % options.person
	# print 'Fruit flies like %s' % options.query
	print 'opt_args %s' % options.opt_args
	# print 'file name %s' % options.filename
	if options.bool: 
		print 'print documentation' 
		print main.__doc__
		print "for operating information type '%s -h'" % __file__

if __name__ == '__main__':
	print "starting"
	main()
	print "that's it"


