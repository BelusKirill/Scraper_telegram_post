from datetime import datetime
from dateutil.parser import parse
from tzlocal import get_localzone #pip install tzlocal /для часового пояса
from dbconnect import get_data_line

import time

# получаем текущий часовой пояс
tz = get_localzone()

def check_data(date: datetime, name_channel: str) -> bool:
    cdate: datetime = None
    rdate = get_data_line(f"SELECT date FROM history_appeals where channel = '{name_channel}'")    

    if rdate == None:
        cdate = datetime(year=datetime.now().year, 
                month=datetime.now().month, 
                day=datetime.now().day, 
                hour=0, 
                minute=0)
    else:
        cdate = parse(rdate[0])

    dt = date.astimezone(tz)

    return cdate.timestamp() < dt.timestamp()