import yaml
import time
from os import path
from datetime import datetime
import XiaoYiJiang
import Schedule
import sys


scriptFolderPath = sys.path[0]

excelFilePath = path.join(scriptFolderPath,"example.xlsx")

# read config from config.yaml
with open("_config.yaml") as f:
    config = yaml.load(f.read(),Loader=yaml.loader.Loader)
    config["TOUSER"] = "|".join(config["TOUSER"])

my_schedule = Schedule.Schedule(excelFilePath)
XiaoYi = XiaoYiJiang.XiaoYiJiang(config["CORPID"],config["CORPSECRET"],config["AGENTID"],config["TOUSER"],scriptFolderPath)
XiaoYi.get_accessToken()

i = 0 # FIXME for test
while True:
    
    time.sleep(1)
    i += 1