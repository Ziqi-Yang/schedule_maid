from pandas import read_excel
from datetime import datetime
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
        self.scheduled_times = scheduleTime.ScheduleTime(self.schedule.index[1:])
    

    def getTodaySch(self,weekday):
        self.todaySch = self.schedule.iloc[:,weekday]

    def parseCell(self,text):
        lines =  text.split("\n")
        mode = lines[0] if lines[0] in ["[multi]","[section]"] else None
        if mode == None: # normal Cell
            message = "\n".join(lines)
            for line in lines:
                if line.startswith("[") and line.endswith("]"):
                    continue
                else:
                    self.parseLine()
        else:
            if mode == "[multi]":
                pass
            elif mode == "[section]":
                pass
    
    def parseLine(self,line):
        line = line.strip()
        tmp = re.findall(r"(\d{2}[.:]\d{2})\s[-](\d{2}[.:]\d{2})",line)
        if len(tmp) == 1:
            tmp = [i for x in tmp for i in x]
            if len(tmp) != 2:
                raise Exception("the format of {} is not vailed".format(line))
            else:
                if tmp[0] != tmp[1]:
                    timeStr_lastPosPlus1 = re.search(tmp[1],line).span()[-1]
                    
                    print(tmp[0],tmp[1],line,timeStr_lastPosPlus1)
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
    sch.check_sch()
    sch.parseLine(" 16.00 -17:00鸟哥的Linux私房菜")