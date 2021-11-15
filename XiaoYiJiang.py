import requests
from time import time
import pickle
import sys
from os import path


class XiaoYiJiang:
    def __init__(self,CORPID,CORPSECRET,AGENTID,TOUSER):
        self.CORPID = CORPID
        self.CORPSECRET = CORPSECRET
        self.AGENTID = AGENTID
        self.TOUSER = TOUSER # str value, e.x. "aaa|bbbb"
        self.ACCESS_TOKEN = None # need to get

        self.token_expires_time = 7200 #ACCESS_TOKEN expires_time
        self.scriptFolderPath = sys.path[0]
        self.tokenFilePath = path.join(self.scriptFolderPath, "token_time_log.pkl")
        self.daily_greetings = "主人，今天又是新的一天。干劲满满哦！"
    
    def checkTime(self,curTime):
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
        if self.checkTime(curTime) == False:
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(self.CORPID,self.CORPSECRET)
            rq = requests.get(url).json()
            # return rq.json
            self.ACCESS_TOKEN = rq["access_token"]

    # def sendMessage(message):
        

if __name__ == "__main__":
    xiaoYi = XiaoYiJiang("ww467b245fc82994a0","jGOo-_mBrGbLTwrxwnUtYAYcljys4Dx8FLQDM8HUWsE",1000002,"YangZiQi")
    xiaoYi.get_accessToken()
    print(xiaoYi.ACCESS_TOKEN)