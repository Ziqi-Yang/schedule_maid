import datetime

sch_time = "00:51"
converted_time = datetime.datetime.strptime(sch_time,"%H:%M")
converted_time1 = datetime.datetime.strptime("00:20","%H:%M")
print(converted_time , converted_time1)
print(datetime.datetime.today().weekday())

timeStr = [" 00.30 -00.49","00.49- 00.61","23:40-00:12","00.12-00:15","00:19-00.16","00.19-00.31"]

for x in timeStr:
    