import requests
from time import time
from datetime import datetime
import pickle
import sys
from os import error, path
import json


class XiaoYiJiang:
    def __init__(self,CORPID,CORPSECRET,AGENTID,TOUSER,scriptFolderPath):
        self.CORPID = CORPID
        self.CORPSECRET = CORPSECRET
        self.AGENTID = AGENTID
        self.TOUSER = TOUSER # str value, e.x. "aaa|bbbb"
        self.ACCESS_TOKEN = None # need to get

        self.token_expires_time = 7200 #ACCESS_TOKEN expires_time
        self.scriptFolderPath = scriptFolderPath
        self.tokenFilePath = path.join(self.scriptFolderPath, "token_time_log.pkl")
        self.morning_greeting = "主人，今天又是新的一天。干劲满满哦！"
    
    def checkToken(self,curTime):
        """check if current time is in the token expires time"""
        if path.exists(self.tokenFilePath):
            token_time = pickle.load(open(self.tokenFilePath,"rb"))
            if curTime - token_time < self.token_expires_time and self.ACCESS_TOKEN != None:
                return True
            elif self.ACCESS_TOKEN == None:
                return False
        pickle.dump(time(),open(self.tokenFilePath,"wb"))
        return False
    
    def get_accessToken(self):
        curTime = time()
        if self.checkToken(curTime) == False:
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(self.CORPID,self.CORPSECRET)
            rq = requests.get(url).json()
            # return rq.json
            self.ACCESS_TOKEN = rq["access_token"]
    
    def writeLog(self,log):
        with open(path.join(self.scriptFolderPath,"XiaoYi.log"),"a") as f:
            f.writelines("[{}] {}]".format(datetime.now(),log))

    def sendMessage(self,markdown):
        tmpMsg = {
            "touser" : self.TOUSER,
            "msgtype": "markdown",
            "agentid": self.AGENTID,
            "markdown": {
                "content": markdown
            }
        }
        newMessage = bytes(json.dumps(tmpMsg),"utf-8")
        self.get_accessToken()
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(self.ACCESS_TOKEN)
        rq = requests.post(url,newMessage).json()
        if rq["errcode"] != 0:
            self.writeLog("ErrorCode: {}\n{}\n".format(rq["errcode"],rq["errmsg"]))




        

if __name__ == "__main__":
    # FIXME need to detele before public
    xiaoYi = XiaoYiJiang("ww467b245fc82994a0","jGOo-_mBrGbLTwrxwnUtYAYcljys4Dx8FLQDM8HUWsE",1000002,"YangZiQi",sys.path[0])
    xiaoYi.get_accessToken()
    message="""`Hello` Sir!""" 
    xiaoYi.sendMessage(message)
