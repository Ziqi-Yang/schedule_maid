import requests


class XiaoYiJiang:
    def __init__(self,CORPID,CORPSECRET,AGENTID,TOUSER):
        # NOTICE nedd to delete these lines before  publish
        self.CORPID = "ww467b245fc82994a0"
        self.CORPSECRET = "jGOo-_mBrGbLTwrxwnUtYAYcljys4Dx8FLQDM8HUWsE"
        self.ACCESS_TOKEN = None

        # self.CORPID = CORPID
        # self.CORPSECRET = CORPSECRET
        # self.AGENTID = AGENTID
        # self.TOUSER = TOUSER # str value, e.x. "aaa|bbbb"

        self.daily_greetings = "主人，今天又是新的一天哦。干劲满满！"

    def get_accessToken(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(self.CORPID,self.CORPSECRET)
        rq = requests.get(url)
        # return rq.json
        self.ACCESS_TOKEN = rq.json()["access_token"]

    # def sendMessage(message):
        

if __name__ == "__main__":
    xiaoYi = XiaoYiJiang()
    xiaoYi.get_accessToken()
    print(xiaoYi.ACCESS_TOKEN)