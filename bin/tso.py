import sys
orig_stdout = sys.stdout
f = file('out.txt', 'w')
sys.stdout = f
print 'Hello World to file'
sys.stdout = orig_stdout
f.close()
print 'Hello World to screen'
