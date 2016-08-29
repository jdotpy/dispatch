# dispatch
Python package for timed dispatching of events or work

# Example usage:
	import time
	from dispatch import Reactor

	# Some example functions
	def work():
		time.sleep(2)
		print('work done!')
	
	# To Print "hi" every 2 seconds
	r = Reactor()
	r.dispatch(
		r.schedule_interval(seconds=2), 
		r.action(print, 'hello') # this will be done in main thread and will interfere with main loop
	)
	r.run()

	# To trigger a 2-second work function every second
	r = Reactor()
	r.dispatch(
		r.schedule_interval(seconds=1), 
		r.backgound_action(work)  # this will be done in a separate thread and wont interfere with main loop
	)
	r.run()
