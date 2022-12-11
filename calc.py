from datetime import datetime
from tzlocal import get_localzone #pip install tzlocal /для часового пояса

import time

# получаем текущий часовой пояс
tz = get_localzone()

def check_data(date: datetime) -> bool:
    cdate = datetime(year=datetime.now().year, 
            month=datetime.now().month, 
            day=datetime.now().day, 
            hour=0, 
            minute=0)

    dt = date.astimezone(tz)

    return cdate.timestamp() < dt.timestamp()