import yaml
import time
from os import path
from datetime import date, datetime
import XiaoYiJiang
import Schedule
import sys


scriptFolderPath = sys.path[0]

excelFilePath = path.join(scriptFolderPath,"example.xlsx")

# read config from config.yaml
with open("_config.yaml") as f: # FIXME change _config.yaml to config.yaml
    config = yaml.load(f.read(),Loader=yaml.loader.Loader)
    config["TOUSER"] = "|".join(config["TOUSER"])


my_schedule = Schedule.Schedule(excelFilePath)
XiaoYi = XiaoYiJiang.XiaoYiJiang(config["CORPID"],config["CORPSECRET"],config["AGENTID"],config["TOUSER"],scriptFolderPath)
XiaoYi.get_accessToken()

while True:
    # timeStr = datetime.now().strftime("%H:%M")
    timeStr = "06:55"
    sch = my_schedule.querySch(timeStr)
    if sch != None:
        message = ""
        if sch[0] == 0:
            XiaoYi.sendMessage(XiaoYi.morning_greeting,type="text")
            XiaoYi.sendMessage(my_schedule.formatTodaySch(type=2))
        XiaoYi.sendMessage(sch[1])
        time.sleep(11 * 60)
    time.sleep(60)