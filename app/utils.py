from datetime import datetime
import time
from typing import Optional


def get_timestamp(datetime0: Optional[datetime] = None) -> int:
    if datetime0 is None:
        datetime0 = datetime.now()
    return int(datetime0.timestamp() * 1000)


def get_datetime(timestamp: Optional[int] = None) -> datetime:
    if timestamp is None:
        timestamp = int(time.time() * 1000)
    return datetime.fromtimestamp(timestamp)
