from pandas import read_excel
from datetime import datetime


class Schedule:
    def __init__(self,excel_path):
        self.schedule = read_excel(excel_path,engine="openpyxl",index_col=0)
        self.weekdays = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日",]

    def check_sch(self):
        """ check the schedule sheet for compliance
        supported label: "multi","section"
            "multi": a single cell contains multi tasks
            "section": combine the current cell with the lower cell(lower cell should be blank or has "section" label only)
        anything in the brackets will be ignored when parsing, but them will be in the body message(i.e. they will be sent)
        """
    def str2time(timeStr) -> *datetime:
        """check string format and time overlaps"""
        pass
        

    
    def getTodaySch(self,weekday):
        self.todaySch = self.schedule[self.weekdays[weekday]]
        
    
if __name__ == "__main__":
    sch = Schedule("example.xlsx")
    weekday = datetime.today().weekday()
    print(sch.schedule)
