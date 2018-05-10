from datetime import datetime, timedelta, date
import time

def daterange(date1, date2):
    for n in range(((date2 - date1).days)+1):
         print date2
         yield date1 + timedelta(n)
#starttime = datetime.now()
#enddate1 = time.strftime("%m/%d/%Y", time.localtime(time.time()))
#fromdate1 = time.strftime("%m/%d/%Y", time.localtime(starttime))
start_dt = date(2017, 2, 12)
end_dt = date(2018, 2, 12)
print start_dt
print end_dt
for dt in daterange(start_dt, end_dt):
    print(dt.strftime("%Y-%W"))
	
