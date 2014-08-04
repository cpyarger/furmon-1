#/usr/bin/env python
#
# Reads binary data, splits it into a list of lines and prints the
# list, thusly:
#
# ["Ipsum lorem.", "..."]
#

def qwert():
    fin = open("flint.txt","rb")
    return fin

def asdf(a_file):
    buf   = a_file.read()    # swallow the whole file
    lines = buf.split("\n")  # split it into lines 
    return lines

my_file = qwert()
print asdf(my_file)
