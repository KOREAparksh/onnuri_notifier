import slack_sdk
import datetime as dt
from datetime import timedelta
import os
import sys


weekdays = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일",
}

    

#낮에 보내는 당일 점심 
def slackBlockLaunchFormat():
    today = dt.datetime.now()
    weekday = today.weekday()
    today = today.strftime("%y년 %m월 %d일 " + weekdays[weekday])

    title = "🤩  `" + today + "` 오늘의 점심 메뉴는???\n오늘 점심 맛있게 먹고 오후도 화이팅!!!\n"
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": title
            }
        }
    ]

    
def slackErrorMessageFormat(msg):
    today = dt.datetime.now()
    today = today.strftime("%y년 %m월 %d일")

    return [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":alert: `Error` 메뉴를 불러오지 못했습니다.\n```" + today + "\n" + msg + "```"
			}
		},
    ]

def sendSlackLaunchMessage(imageUrls, slackToken, channel) :
    path = sys.argv[2]
    print("path: ", path)
    client = slack_sdk.WebClient(token = slackToken)
    os.system("mkdir -p {}/image".format(path))
    
    # 메세지 입력
    index = 0
    message = "🤩 온누리식당 메뉴 알림!\n"
    for imageUrl in imageUrls:
        os.system("curl " + imageUrl + " > " + "{}/image/{}.png".format(path, index))
        image = open("{}/image/{}.png".format(path, index), 'rb')
        upload = client.files_upload(file=image)
        message += "<" + upload["file"]["permalink"] + "| >"
        index += 1
    
    client.chat_postMessage(channel = channel, text=message, blocks = slackBlockLaunchFormat())
    os.system("rm -rf " + path)

def sendSlackErrorMessage(msg, slackToken, channel) :
    client = slack_sdk.WebClient(token = slackToken)
    client.chat_postMessage(channel = channel, blocks = slackErrorMessageFormat(msg))
