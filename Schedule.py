from pandas import read_excel
import pandas as pd
from datetime import datetime
import pickle

from pandas.core.frame import DataFrame
import scheduleTime
import re




class Schedule:
    def __init__(self,excel_path):
        self.schedule = read_excel(excel_path,engine="openpyxl")
        self.checkSch()
        self.getTodaySch(datetime.today().weekday())

    def checkSch(self):
        """ check the schedule sheet for compliance"""
        time_intervals = scheduleTime.ScheduleTime(self.schedule.iloc[1:,0]).schedule
        self.schedule.insert(self.schedule.shape[1],"time_intervals",[None]+time_intervals)
    
    def replaceLine(self,df,i,dfLines):
        df1 = df.iloc[:i,:]
        df2 = df.iloc[i+1:,:]
        return pd.concat([df1,dfLines,df2],ignore_index=True)


    def getTodaySch(self,weekday):
        weekdayMap = {0:"星期一",1:"星期二",2:"星期三",3:"星期四",4:"星期五",5:"星期六",6:"星期日"}
        self.weekday = weekdayMap[weekday]
        self.todaySch = self.schedule[["time_intervals",self.weekday]]
        self.todayNotice = self.schedule.iloc[0,weekday+1]
        self.schedule = self.todaySch.drop([0]) # drop notice, don't use inplace parameter because of some rules
    
    def parseCells():
        """
        supported label: "multi","section"
            "multi": a single cell contains multi tasks
            "section": combine the current cell with the lower cell(lower cell should be blank or has "section" label only)
        anything in the brackets will be ignored when parsing, but them will be in the body message(i.e. they will be sent)
        """
        pass

    def parseSingleCell():
        pass
    
    def querySch(self,time:datetime):
        pass
        
        
    
if __name__ == "__main__":
    sch = Schedule("example.xlsx")
    print(sch.schedule)

    # sch.getTodaySch(weekday)