from .core import Reactor 

def main():
    r = Reactor()
    r.dispatch(
        r.schedule_calendar(hours=[4, 21]),
        r.action(print, 'hi')
    )
    r._debug()
    print('done')


if __name__ == '__main__':
    main()
