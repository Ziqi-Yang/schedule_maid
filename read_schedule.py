from pandas import read_excel
from datetime import datetime
import scheduleTime



class Schedule:
    def __init__(self,excel_path):
        self.schedule = read_excel(excel_path,engine="openpyxl",index_col=0)

    def check_sch(self):
        """ check the schedule sheet for compliance
        supported label: "multi","section"
            "multi": a single cell contains multi tasks
            "section": combine the current cell with the lower cell(lower cell should be blank or has "section" label only)
        anything in the brackets will be ignored when parsing, but them will be in the body message(i.e. they will be sent)
        """
        self.scheduled_times = scheduleTime.ScheduleTime(self.schedule.index[1:])
    
    def getTodaySch(self,weekday):
        self.todaySch = self.schedule.iloc[:,weekday]
        
    
if __name__ == "__main__":
    sch = Schedule("example.xlsx")
    weekday = datetime.today().weekday()
    sch.getTodaySch(weekday)
    sch.check_sch()
    print(sch.todaySch)