from pandas import read_excel
from pandas import isnull
import pandas as pd
from datetime import datetime,timedelta
import re
import scheduleTime




class Schedule:
    def __init__(self,excel_path,advancedRdTime = 10*60):
        self.advancedRdTime = advancedRdTime # advanced remind time (seconds)
        self.excelPath = excel_path
        self.schedule = read_excel(excel_path,engine="openpyxl")
        self.initialize()

    def initialize(self):
        print("[*] Read excel file {} done. Start initialization.".format(self.excelPath))
        self.checkSchTime()
        self.testSch()
        self.parseCells()



    def checkSchTime(self):
        """ check the schedule sheet for compliance"""
        time_intervals = scheduleTime.ScheduleTime(self.schedule.iloc[1:,0]).schedule
        self.schedule.insert(self.schedule.shape[1],"time_intervals",[None]+time_intervals)
    
    def addSchedule(self,i,dfLines,mode=1):
        df1 = self.todaySch.iloc[:i,:]
        if mode == 1: # replace
            df2 = self.todaySch.iloc[i+1:,:]
        elif mode == -1: # insert
            df2 = self.todaySch.iloc[i:,:]
        else:
            raise Exception("addSchdule Function doesn't support mode {}".format(mode))
        self.todaySch = pd.concat([df1,dfLines,df2],ignore_index=True)



    def getTodaySch(self,weekday):
        """
        must have weekday parameter, for testSch function
        """
        weekdayMap = {0:"星期一",1:"星期二",2:"星期三",3:"星期四",4:"星期五",5:"星期六",6:"星期天"}
        self.weekday = weekdayMap[weekday]
        self.todaySch = self.schedule[["time_intervals",self.weekday]]
        self.todayNotice = self.schedule.iloc[0,weekday+1]
        self.todaySch = self.todaySch.drop([0]) # drop notice, don't use inplace parameter because of some rules
        self.todaySch.index = range(self.todaySch.shape[0]) # let index start from zero
    
        

    
    def parseCells(self):
        """
        supported label: "multi","section"
            "multi": a single cell contains multi tasks
            "section": combine the current cell with next cell(lower cell should be blank or has "section" label only)
        anything in the brackets will be ignored when parsing, but them will be in the body message(i.e. they will be sent)
        """
        index = 0
        while index < self.todaySch.shape[0]:
            if index == 13:
                print(self.todaySch)
            cell = self.todaySch[self.weekday][index]
            if isnull(cell):
                continue
            cellLines = cell.strip().split("\n")
            cellMode = cellLines[0][1:-1] if cellLines[0].strip() in ["[multi]","[section]"] else None
            if cellMode == None:
                pass
            elif cellMode == "multi":
                addScheduleMode = 1
                indexOverPlus = 0 # avoid indexOverplus, value could be 0 or 1
                for line in cellLines:
                    line = line.strip()
                    if line[0] == "[" and line[-1] == "]":
                        continue
                    elif re.match(r"\d{2}[.:]\d{2}",line[:5]) != None:
                        if re.match(r"(\d{2}[.:]\d{2})-(\d{2}[.:]\d{2})",line[:11]) == None:
                            raise Exception("the format of the cell contains an error:\n{}".format(cell))

                        timeInterval = scheduleTime.TimeInterval(line[:11]).time_interval
                        newSchduleContent = line[11:].strip()
                        newSchdule = pd.DataFrame([[timeInterval,newSchduleContent]],columns=["time_intervals",self.weekday])
                        self.addSchedule(index,newSchdule,mode=addScheduleMode)
                        if addScheduleMode == -1:
                            indexOverPlus = 1
                        addScheduleMode = -1 if addScheduleMode == 1 else -1 # only change once
                        index += 1
                index -= indexOverPlus
                        

            elif cellMode == "section":
                schedule = ""
                if index == self.todaySch.shape[0] - 1:
                    raise Exception("the [section] label couldn't be replaced in the last schdule")
                for line in cellLines:
                    line = line.strip()
                    if line[0] == "[" and line[-1] == "]":
                        continue
                    else:
                        schedule += line + "\n"
                if len(schedule) != 0:
                    schedule = schedule[:-1] # delete "\n"
                self.todaySch[self.weekday][index] = schedule
                self.todaySch[self.weekday][index + 1] = "继续-" + schedule
            index += 1
        scheduleTime.checkCorrect(list(self.todaySch["time_intervals"])) # check for time overlap

    def testSch(self):
        """
        simulate the real excution, and ouput the all days's modified schdule respectively into one file
        """
        print("[*] Start testing excel file, which may takes some time.")
        for i in range(7):
            self.getTodaySch(i)
            self.parseCells()
        # restore to today's situation
        self.getTodaySch(datetime.today().weekday())
        self.parseCells()
        print("[*] Test finished. All things are in the right format.")
    
    def querySch(self,timeStr):
        """
        timeStr format: '%H:%M' , for example '01:02'
        NOTICE when in main function in time loop, we need to add sleep(10 * 60)
        return:
            - index of schedule
            - schedule content
        """
        def between(time,schIndex):
            # schIndex is the label name(start from 1)
            time_interval = self.todaySch["time_intervals"][schIndex]
            if time >= time_interval[0] + timedelta(seconds=-self.advancedRdTime) and time < time_interval[0]:
                return True
            else:
                return False
        # print("[*] Query time {}".format(timeStr))
        theTime = scheduleTime.parseTime(timeStr) # check also included in the function
        if between(theTime,0):
            self.getTodaySch(datetime.today().weekday()) # update
            self.parseCells()
        
        for i in range(self.todaySch.shape[0]):
            if between(theTime,i):
                return i,self.todaySch[self.weekday][i]

    def formatTodaySch(self,type=1):
        def format_TimeIntervals(timeIntervals:list):
            res = []
            for time_interval in timeIntervals:
                tmp_TI = [time_interval[i].strftime("%H:%M") for i in range(2)]
                res.append("-".join(tmp_TI))
            return res
        todaySch = self.todaySch.copy()
        todaySch["time_intervals"] = format_TimeIntervals(todaySch["time_intervals"])
        todaySch.columns = ["时间","安排"]
        todaySch.set_index("时间",inplace=True)
        res = "今天({})的安排: \n {}\n".format(self.weekday,self.todayNotice)
        if type == 1:
            """
            12:13-13:13 xxx
                        xxx
            12:13-13:13 xxx
                        xxx
            """
            
            for x in todaySch.index:
                tasks = todaySch.loc[x][0]
                if isnull(tasks):
                    tasks = ""
                tasks = tasks.split("\n") # shouldn't use raw string
                res += x + " "
                res += tasks[0] + "\n"
                if len(tasks) > 1:
                    for task in tasks[1:]:
                        res += " " * (len(x) + 1)
                        res += task + "\n"
        elif type == 2:
            """
            12:13-13:13
             xxx
             xxx

            12:13-13:13
             xxx
             xxx
            """
            for x in todaySch.index:
                tasks = todaySch.loc[x][0]
                if isnull(tasks):
                    tasks = ""
                tasks = tasks.split("\n") # shouldn't use raw string
                res += x + "\n"
                res += " " + tasks[0] + "\n"
                if len(tasks) > 1:
                    for task in tasks[1:]:
                        res += " " + task + "\n"
                res += "\n"
        else:
            raise Exception("Unsupported function parameter type={}".format(type))
        return res
            


        
    
if __name__ == "__main__":
    sch = Schedule("example.xlsx")
    print(sch.formatTodaySch())
    print(sch.todaySch)
    # print(sch.querySch("22:59"))

    # sch.getTodaySch(weekday)