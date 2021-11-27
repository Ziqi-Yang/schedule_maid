import requests
from time import time
from datetime import datetime
import pickle
from os import path
import json
from random import choice


class XiaoYiJiang:
    def __init__(
        self,
        CORPID,
        CORPSECRET,
        AGENTID,
        TOUSER,
        scriptFolderPath,
        ana: list,
        nickname="主人",
        morningGreeting="今天又是新的一天。干劲满满哦！来看看今天的计划吧！",
    ):
        self.CORPID = CORPID
        self.CORPSECRET = CORPSECRET
        self.AGENTID = AGENTID
        self.TOUSER = TOUSER  # str value, e.x. "aaa|bbbb"
        self.ACCESS_TOKEN = None  # need to get

        self.token_expires_time = 7200  # ACCESS_TOKEN expires_time
        self.scriptFolderPath = scriptFolderPath
        self.tokenFilePath = path.join(self.scriptFolderPath, "token_time_log.pkl")
        self.errorLog = path.join(self.scriptFolderPath, "XiaoYi.log")

        self.nickname = nickname  # your nickname
        self.morning_greeting = self.nickname + "，" + morningGreeting
        # with open(path.join(self.scriptFolderPath, ana), "r", encoding="UTF-8") as f:
        #     self.prompts = f.readlines()
        #     self.prompts = [self.prompts[i][:-1] for i in range(len(self.prompts))]
        self.prompts = ana

    def checkToken(self, curTime):
        """check if current time is in the token expires time"""
        if path.exists(self.tokenFilePath):
            token_time = pickle.load(open(self.tokenFilePath, "rb"))
            if (
                curTime - token_time < self.token_expires_time
                and self.ACCESS_TOKEN != None
            ):
                return True
            elif self.ACCESS_TOKEN == None:
                return False
        pickle.dump(time(), open(self.tokenFilePath, "wb"))
        return False

    def get_accessToken(self):
        curTime = time()
        if self.checkToken(curTime) == False:
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(
                self.CORPID, self.CORPSECRET
            )
            rq = requests.get(url).json()
            # return rq.json
            self.ACCESS_TOKEN = rq["access_token"]

    def writeLog(self, log):
        with open(self.errorLog, "a") as f:
            f.writelines("[{}] {}]".format(datetime.now(), log))

    def randomPrompt(self):
        return self.nickname + "，" + choice(self.prompts)

    def sendMessage(self, message: str, type="markdown"):
        """
        type: "text", "markdown"
        """
        if type not in ["text", "markdown"]:
            raise Exception("Unsupported function parameter 'type'")
        self.get_accessToken()  # check token
        print("[*] Check access token done.")
        print(
            "[{}] Send schedule remind message.".format(
                datetime.now().strftime("%H:%M")
            )
        )
        if type == "markdown":
            message = message[:-1] if message[-1] == "\n" else message
            message = "`" + message + "`\n"
            message += "\n" + self.randomPrompt()

        tmpMsg = {
            "touser": self.TOUSER,
            "msgtype": type,
            "agentid": self.AGENTID,
            type: {"content": message},
        }
        newMessage = bytes(json.dumps(tmpMsg), "utf-8")
        self.get_accessToken()
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(
            self.ACCESS_TOKEN
        )
        rq = requests.post(url, newMessage).json()
        if rq["errcode"] != 0:
            self.writeLog("ErrorCode: {}\n{}\n".format(rq["errcode"], rq["errmsg"]))
            print("[******] Error occured. See errors in the {}".format(self.errorLog))
        # return rq["msgid"]


if __name__ == "__main__":
    pass
