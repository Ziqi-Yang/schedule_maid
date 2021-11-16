from pandas import read_excel
import pandas as pd
from datetime import datetime

from pandas.core.frame import DataFrame
import scheduleTime
import re




class Schedule:
    def __init__(self,excel_path):
        self.schedule = read_excel(excel_path,engine="openpyxl",index_col=r"时间\星期")


    def check_sch(self):
        """ check the schedule sheet for compliance
        supported label: "multi","section"
            "multi": a single cell contains multi tasks
            "section": combine the current cell with the lower cell(lower cell should be blank or has "section" label only)
        anything in the brackets will be ignored when parsing, but them will be in the body message(i.e. they will be sent)
        """
        # FIXME need to support label
        self.scheduled_times = scheduleTime.ScheduleTime(self.schedule.index[1:]).schedule
    
    def replaceLine(self,df,i,dfLines):
        df1 = df.iloc[:i,:]
        df2 = df.iloc[i+1:,:]
        return pd.concat([df1,dfLines,df2],ignore_index=True)


    def getTodaySch(self,weekday):
        self.check_sch()
        weekdayMap = {0:"星期一",1:"星期二",2:"星期三",3:"星期四",4:"星期五",5:"星期六",6:"星期日",}
        self.weekday = weekdayMap[weekday]
        self.todaySch = pd.DataFrame(self.schedule.iloc[:,weekday])
        self.todayNotice = list(self.todaySch.iloc[0,:])[0]
        self.todaySch.drop([self.todaySch.index[0]],inplace=True)
    

    def parseCell(self,text,sch_number):
        lines = text.split("\n")
        mode = lines[0] if lines[0] in ["[multi]","[section]"] else None
        if mode != None:
            if mode == "[multi]":
                pdLines = pd.DataFrame([])
                time_intervals = []
                for line in lines:
                    pdLine,time_interval = self.parseLine(line)
                    pdLines =  pdLines.append(pdLine,ignore_index=True)
                    time_intervals.append(time_interval)

                self.todaySch = self.replaceLine(self.todaySch,sch_number,pdLine)
                index = sch_number
                self.scheduled_times.pop(sch_number)
                for time_interval in time_intervals:
                    self.scheduled_times.insert(index,time_intervals)
                    index += 1    

            elif mode == "[section]":
                pass
    
    def parseLine(self,line):
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            return
        tmp = re.findall(r"(\d{2}[.:]\d{2})\s[-](\d{2}[.:]\d{2})",line)
        if len(tmp) == 1:
            tmp = [i for x in tmp for i in x]
            if len(tmp) != 2:
                raise Exception("the format of {} is not vailed".format(line))
            else:
                if tmp[0] != tmp[1]:
                    timeStr_lastPosPlus1 = re.search(tmp[1],line).span()[-1]
                    timeInterval = scheduleTime.TimeInterval(line[:timeStr_lastPosPlus1]).time_interval
                    task = line[timeStr_lastPosPlus1:]
                    # FIXME pd
                    pdLine =pd.DataFrame([task],columns=[self.weekday],index=["-".join(tmp)])
                    return pdLine,timeInterval
                    # self.todaySch = self.replaceLine(self.todaySch,line_index,pdLine,timeInterval)
                else:
                    raise Exception("{} contains same timeString".format(line))
        else:
            
            raise Exception("the format of {} is not vailed".format(line))
    
    def querySch(self,time:datetime):
        pass
        
        
    
if __name__ == "__main__":
    sch = Schedule("example.xlsx")
    weekday = datetime.today().weekday()
    sch.getTodaySch(weekday)
    # pdLine = DataFrame(["Hello"],index=["8:00-9:00"])
    sch.parseLine(0," 16.00 -17:00鸟哥的Linux私房菜")
    # print(sch.replaceLine(sch.todaySch,1,pdLine))
    print(sch.todaySch)
    print(sch.scheduled_times)