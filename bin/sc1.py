#!/usr/bin/python
import sys				# load the system module
marker = ":"*10 + 'textpak=>'		# hopefully unique 

def pack():
	for name in sys.argv[1:]:	# for all command-line arguments
		input = open(name, 'r')	# open the next input file
		print marker + name 	# write a separator line
		print input.read(),	# and write the files contents

if __name__== '__main__': pack()	# if this is the main function run stand alone...
