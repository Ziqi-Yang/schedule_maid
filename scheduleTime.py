from datetime import datetime
import re


class ScheduleTime:
    def __init__(self,timeIntervals: list):
        self.schedule = [TimeInterval(x).time_interval for x in timeIntervals]
        formerTime = datetime.strptime("00:00","%H:%M")
        for index in range(len(self.schedule)-1):
            time_interval = self.schedule[index]
            if time_interval[0] >= time_interval[1] and index <= len(self.schedule)//2: # normally the former half of time interval don't across a day
                raise Exception("the num {} of the given time Strings is not available, for the former one should be earlier than the latter one".format(index + 1))
            if time_interval[0] < formerTime:
                raise Exception("Time overlaped!")
            formerTime = time_interval[1]
        if self.schedule[-1][0] < formerTime:
            raise Exception("Time overlaped!")
        if self.schedule[-1][1] >= self.schedule[0][0]:
            raise Exception("Time overlaped!")

class TimeInterval:
    def __init__(self,timeInterval: str):
        timeInterval = timeInterval.replace(" ","")
        if "-" not in timeInterval:
            raise Exception("The format of {} is not allowed.".format(timeInterval))
        self.time_interval = [self.parseTime(x) for x in timeInterval.split("-")]
        
    def parseTime(self,timeStr):
        if re.match(r"\d{2}[.:]+\d{2}",timeStr) == None:
            raise Exception("The format {} is not allowed.".format(timeStr))
        timeStr = timeStr.replace(".",":")
        for x in timeStr.split(":"):
            if int(x) >= 60:
                raise Exception("{} is not valid,time inverval should contain numbers < 60".format(timeStr))
        return datetime.strptime(timeStr,"%H:%M")
        

if __name__ == "__main__":
    timeStr = [" 00.30 -00.49","00.49- 00.59","00.59-01.10","01.10-01.11","01.11-01.12","01.13-00.29"]
    timeStr_1 = [" 00.30 -00.49","00.49- 00.59","00.59-01.10","01.09-01.11","01.11-01.12","01.12-00.29"]
    x = ScheduleTime(timeStr_1)
    for x in x.schedule:
        print(x.time_interval)