def dfout:
	''' display filtered output '''
	# output of objects test point
	# print c.alarm.__doc__ ," The value is",(alarm(L))
	# print c.state.__doc__ ," The value is",(state(L))
	print(alarm(L))
	print(state(L))
	print(ophours(L))
	print(resets(L))
	print(starts(L))
	print(systmp(L))
	print(stacktmp(L))
	print(thstcall(L))
	# print c.thstcall.__doc__ ," The value is",(thstcall(L))
	# print c.ignind.__doc__ ," The value is",(ignind(L)) # currently dumps L
	print "tada display"

