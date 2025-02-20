import datetime
from pytz import timezone, utc


def get_local_time(time_zone) -> str:
    now_utc = datetime.datetime.now(utc)
    local_timezone = timezone(time_zone)
    now_local = now_utc.astimezone(local_timezone)
    timestamp_str = now_local.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp_str


__all__ = ["get_local_time"]
