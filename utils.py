from datetime import datetime
import time


def get_timestamp(datetime0: datetime = None) -> int:
    if datetime0 is None:
        datetime0 = datetime.now()
    return int(datetime0.timestamp() * 1000)


def get_datetime(timestamp: int = None) -> int:
    if timestamp is None:
        timestamp = int(time.time() * 1000)
    return datetime.fromtimestamp(timestamp)
