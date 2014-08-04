#!/usr/bin/env python
import optparse
import subprocess


def main():
    	p = optparse.OptionParser(description='A unix testbox',
                                            prog='ibmfr1.py',
                                            version='fits 0.1',
                                            usage= '%prog [option]')
	# p = optparse.OptionParser()
        p.add_option('--verbose', '-v',
                action = 'store_true',
                help='prints verbosely',
                default=False)
	p.add_option('--person', '-p', default="world")
	# p.add_option('--query', '-?', default="world")
	print "starting"
	options, arguments = p.parse_args()
	print 'Hello %s' % options.person
	print "that's it"

if __name__ == '__main__':
	main()
