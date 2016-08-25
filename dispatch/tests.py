from .core import Reactor 

from datetime import datetime, timedelta
import unittest
import time

def example_work():
    time.sleep(3)
    print('work done!')

class Functional(unittest.TestCase):
    def test_basic(self):
        r = Reactor()
        #r.dispatch(
        #    r.schedule_interval(seconds=2, till=datetime.now() + timedelta(seconds=5)),
        #    r.action(lambda: print('hi'))
        #)
        r.dispatch(
            r.schedule_interval(seconds=1), 
            r.background_action(example_work)
        )
        r.run()
