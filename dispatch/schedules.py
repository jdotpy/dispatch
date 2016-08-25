from datetime import timedelta, datetime

def one_time_schedule(timestamp):
    yield timestamp

def interval_schedule(start=None, days=0, hours=0, minutes=0, seconds=0, miliseconds=0, till=None):
    hours += days * 24
    minutes += hours * 60
    seconds += minutes * 60
    interval = seconds + (miliseconds / 1000)
    if start is None:
        start = datetime.now()
    yield start
    current = start
    while True:
        current = current + timedelta(seconds=interval)
        if till and current >= till:
            break
        yield current
