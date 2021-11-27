import yaml
import time
from os import path
from core import XiaoYiJiang
from core import Schedule
import sys
from datetime import datetime


scriptFolderPath = sys.path[0]


# read config from config.yaml
with open("config.yaml", "r", encoding="UTF-8") as f:
    config = yaml.load(f.read(), Loader=yaml.loader.Loader)
    config["TOUSER"] = "|".join(config["TOUSER"])

excelFilePath = path.join(scriptFolderPath, config["excelFilePath"])

my_schedule = Schedule.Schedule(excelFilePath)

XiaoYi = XiaoYiJiang.XiaoYiJiang(
    config["CORPID"],
    config["CORPSECRET"],
    config["AGENTID"],
    config["TOUSER"],
    scriptFolderPath,
    ana=config["XiaoYi"]["ana"],
    nickname=config["XiaoYi"]["nickname"],
    morningGreeting=config["XiaoYi"]["morningGreeting"],
)

XiaoYi.get_accessToken()


while True:
    timeStr = datetime.now().strftime("%H:%M")
    sch = my_schedule.querySch(timeStr)
    if sch != None:
        message = ""
        if sch[0] == 0:
            XiaoYi.sendMessage(XiaoYi.morning_greeting, type="text")
            time.sleep(0.5)  # to avoid message out-of-order
            XiaoYi.sendMessage(my_schedule.formatTodaySch(type=2))
            time.sleep(0.5)
        XiaoYi.sendMessage(sch[1])
        time.sleep(my_schedule.advancedRdTime)
    time.sleep(60)
