from datetime import datetime, timedelta
import threading

from .schedules import one_time_schedule, interval_schedule, CalendarSchedule
import time

class Reactor(): 
    """ The reactor holds the main loop and constructs the plans """

    def __init__(self):
        self.running = False
        self.plans = []

    def run(self):
        self.running = True
        while self.plans:
            now = self.now()
            to_remove = []
            earliest_action = None
            for plan in self.plans:
                # Mark for removal if no future actions need to take place
                if plan.next_run is None:
                    to_remove.append(plan)
                    continue
                # Execute if we've passed the next run time
                elif now >= plan.next_run:
                    plan.run(now)
                # Keep running tab of when the next time i'll have to do something is 
                if earliest_action is None or earliest_action < plan.next_run:
                    earliest_action = plan.next_run

            # Remove plans that are complete
            for plan in to_remove:
                self.plans.remove(plan)

            # Sleep until next action
            if earliest_action:
                sleep_seconds = (earliest_action - self.now()).total_seconds()
                if sleep_seconds > 0:
                    time.sleep(sleep_seconds)
        self.running = False

    def _debug(self, runs=5):
        for plan in self.plans:
            print('------------- Plan {} ---------------'.format(str(plan)))
            for i in range(runs):
                print('Next Run @ {}'.format(str(plan.next_run)))
                plan.get_next_run()

    def now(self):
        return datetime.now()

    def run_in_background(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def dispatch(self, schedule, action, *args, **kwargs):
        self.plans.append(Plan(schedule, action))

    # Shortcuts for actions
    def action(self, func, *args, **kwargs):
        return FunctionCallAction(func, args, kwargs, threaded=False)

    def background_action(self, func, *args, **kwargs):
        return FunctionCallAction(func, args, kwargs, threaded=True)

    # Schedule helpers
    schedule_one_time = one_time_schedule
    schedule_calendar = CalendarSchedule

    def schedule_interval(self, **kwargs):
        if 'start' not in kwargs:
            kwargs['start'] = self.now()
        return interval_schedule(**kwargs)

    def schedule_calendar(self, **kwargs):
        if 'start' not in kwargs:
            kwargs['start'] = self.now()
        return CalendarSchedule(**kwargs)

    def schedule_daily(self, hour=0, minute=0, second=0):
        now = self.now()
        start = now.replace(hour=hour, minute=minute, second=second)
        if start < now:
            start = start + timedelta(days=1)
        return interval_schedule(start=start, days=1)

    def schedule_hourly(self, minute=0, second=0):
        now = self.now()
        start = now.replace(minute=minute, second=second)
        if start < now:
            start = start + timedelta(hours=1)
        return interval_schedule(start=start, hours=1)

class Plan():
    """ A Plan encapsulates the schedule and what is being scheduled. """
    def __init__(self, schedule, action):
        self.schedule = schedule
        self.action = action
        self.last_run = None
        self.next_run = None
        self.get_next_run()

    def get_next_run(self):
        try:
            self.next_run = next(self.schedule)
        except StopIteration:
            self.next_run = None

    def run(self, cycle_time):
        self.last_run = cycle_time
        self.action.run()
        self.get_next_run()

class FunctionCallAction():
    def __init__(self, func, args, kwargs, threaded=False):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.threaded = threaded

    def run(self):
        if self.threaded:
            thread = threading.Thread(target=self.func, args=self.args, kwargs=self.kwargs)
            thread.start()
        else:
            self.func(*self.args, **self.kwargs)
