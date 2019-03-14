from dispatch.core import Reactor

import random
import time

def my_task():
    i = random.randint(1,10000)
    print('Starting task', i)
    time.sleep(10)
    print('Ending task', i)


def main():
    r = Reactor()
    schedule = r.schedule_interval(seconds=2)
    action = r.background_action(my_task)
    r.dispatch(schedule, action)
    r.run()

if __name__ == '__main__':
    main()
