from datetime import date, datetime
from tzlocal import get_localzone
from dbconnect import get_data, get_data_line, insert

tz = get_localzone()
print(tz)
datenow = datetime.now()
datenow.astimezone(tz)
print(datenow)
print(get_data_line('SELECT * FROM "history_appeals"'))

sql = f"INSERT INTO history_appeals (channel, date) VALUES ('{'Название канала'}', '{datetime.now()}')"
insert(sql)
