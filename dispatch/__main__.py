from .core import Reactor 

def main():
    r = Reactor()
    r.dispatch(
        r.schedule_calendar(days_of_week=['Monday'], hours='*'),
        r.action(print, 'hi')
    )
    r._debug()
    print('done')

if __name__ == '__main__':
    main()
