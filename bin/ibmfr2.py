#!/usr/bin/env python
import argparse
import subprocess


def main():
    	p = argparse.OptionParser(description='A unix testbox',
                                            prog='rhcmd.py',
                                            version='rhcme 0.1',
                                            usage= '%prog [option]')
	p = argparse.OptionParser()
	p.add_option('--person', '-p', default="world")
	options, arguments = p.parse_args()
	print 'Hello %s' % options.person

if __name__ == '__main__':
	main()
