import time
STARTTIME=time.time()

import yaml
import time
from os import path
from core import XiaoYiJiang
from core import Schedule
import sys
from datetime import datetime


scriptFolderPath = sys.path[0]


# read config from config.yaml
# with open("config/config.yaml", "r", encoding="UTF-8") as f:
with open("config/private/config.yaml", "r", encoding="UTF-8") as f:
    config = yaml.load(f.read(), Loader=yaml.loader.Loader)
    config["TOUSER"] = "|".join(config["TOUSER"])

# FIXME shoud exmaine config["InUse"] value to determine variable InUseUserFolder
# for loop
InUseUserFolders = ["private"]
# for loop
InUseUserConfig = [
    path.join(
        path.join(path.join(scriptFolderPath, "config"), x), config["excelFileName"]
    )
    for x in InUseUserFolders
]


# FIXME
excelFilePath = path.join(
    path.join(path.join(scriptFolderPath, "config"), "private"), config["excelFileName"]
)
# excelFilePath = path.join(scriptFolderPath, config["excelFileName"])

my_schedule = Schedule.Schedule(excelFilePath)

XiaoYi = XiaoYiJiang.XiaoYiJiang(
    config["CORPID"],
    config["CORPSECRET"],
    config["AGENTID"],
    config["TOUSER"],
    scriptFolderPath=scriptFolderPath,
    ana=config["XiaoYi"]["ana"],
    nickname=config["XiaoYi"]["nickname"],
    morningGreeting=config["XiaoYi"]["morningGreeting"],
)

XiaoYi.get_accessToken()
XiaoYi.sendMessage(XiaoYi.morning_greeting, type="text")


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

ENDTIME=time.time()
print('\n\n')
print('-'*30)
print('Total Time: {}s'.format(ENDTIME-STARTTIME))
