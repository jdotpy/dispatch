# dispatch
Python package for timed dispatching of events or work

# Example usage:
	import time
	from dispatch import Reactor

	reactor = Reactor()
	def hi():
		print('hi')

	def work():
		time.sleep(2)
		print('work done!')
	
	# To Print "hi" every 2 seconds
	# r.action does actions within the main thread
	r = Reactor()
	r.dispatch(
		r.schedule_interval(seconds=2), 
		r.action(hi)
	)

	# To trigger a 2-second work function every second
	# r.background_action spawns a thread for each action
	r = Reactor()
	r.dispatch(
		r.schedule_interval(seconds=1), 
		r.backgound_action(work) 
	)
