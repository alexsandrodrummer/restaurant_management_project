from datetime import datetime, time, timedelta

try:
    from zoneinfo import ZoneInfo
    _TZ = ZoneInfo("Europe/Lisbon")
except Exception:
    _TZ = None


def _now():
    """  """
    return datetime.now(_TZ) if _TZ else datetime.now()

def is_restaurant_open() -> bool:
    """ """

    now = _now()
    weekday = now.weekday() #0=Mon, 6=Sun
    current_t = now.time()


    schedule = {
        0: [(time(9, 0), time(22, 0))], #Mon
        1: [(time(9, 0), time(22, 0))], #tues
        2: [(time(9, 0), time(22, 0))], #wed
        3: [(time(9, 0), time(22, 0))], #thu
        4: [(time(9, 0), time(23, 30))], #fri
        5: [(time(9, 0), time(23, 30))], #Sat
        6: [(time(10, 0), time(21, 0))], #sun
    }
    intervals_today = schedule.get(weekday, [])

    def in_interval(t_open: time, t_close: time) -> bool:
        """
        """
        if t_close > t_open:
            return (current_t >= t_open) or (current_t < t_close)
    
    for (t_open, t_close) in intervals_today:
        if in_interval(t_open, t_close):
            return True

    yesterday = (weekday - 1)%7
    for (t_open, t_close) in schedule.get(yesterday[]):
        if t_close <= t_open:
            if in_interval(t_open, t_close):
                return True
    return False
