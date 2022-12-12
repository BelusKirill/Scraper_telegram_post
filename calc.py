from datetime import datetime
from dateutil.parser import parse
from tzlocal import get_localzone #pip install tzlocal /для часового пояса
from dbconnect import get_data_line

import difflib
import time

# получаем текущий часовой пояс
tz = get_localzone()

def similarity(s1, s2):
    normalized1 = s1
    normalized2 = s2
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()

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

def checking_uniqueness(channels: list, names_channel: list):
    for i in range(0, len(names_channel) - 1, 1):
        if channels[i] == None: continue
        for channel in channels[i]:
            if channel[1] == '': continue
            for j in range(i+1, len(names_channel), 1):
                if channels[j] == None: continue
                for channel2 in channels[j]:
                    res = similarity(channel[1], channel2[1])
                    if res > 0.1:
                        print(res, '|'+channel[1]+"|", "|"+channel2[1]+"|")
