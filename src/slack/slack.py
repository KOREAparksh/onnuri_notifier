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

#밤에 보내는 당일 저녁과 다음날 점심 
def slackMessageDinnerFormat():
    today = dt.datetime.now()
    weekday = today.weekday()
    tomorrow = today + timedelta(days=1)

    today = today.strftime("%y년 %m월 %d일 " + weekdays[weekday])
    tomorrow = tomorrow.strftime("%y년 %m월 %d일 " + weekdays[(weekday + 1) % 7])

    title = "🤩 " +"`" + today + "` 오늘의 저녁 메뉴와\n`" + tomorrow + "` 내일 점심 메뉴는???\n오늘하루 고생많으셨습니다~~!!"
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": title
            }
        }
    ]


#낮에 보내는 당일 점심 
def slackMessageFridayFormat():
    today = dt.datetime.now()
    friday = today + timedelta(days=3)
    friday = friday.strftime("%y년 %m월 %d일 " + weekdays[0])

    title = "🤩  `" + friday + "` 다음주 월요일의 점심 메뉴는???\n행복한 주말 되세요~~!"
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

def sendSlackLaunchMessage(imageUrl, slackToken, channel) :
    path = sys.argv[2]
    client = slack_sdk.WebClient(token = slackToken)
    os.system("mkdir -p {path}/image")
    os.system("curl " + imageUrl + " > " + "{path}/image/image.png")
    image = open("{path}/image/image.png", 'rb')
    upload = client.files_upload(file=image)
    
    message = "🤩 밥플러스 메뉴 알림!\n"
    message += "<" + upload["file"]["permalink"] + "| >"
    
    client.chat_postMessage(channel = channel, text=message, blocks = slackBlockLaunchFormat())
    
    os.system("rm -rf " + "{path}/image/image.png")

def sendSlackErrorMessage(msg, slackToken, channel) :
    client = slack_sdk.WebClient(token = slackToken)
    client.chat_postMessage(channel = channel, blocks = slackErrorMessageFormat(msg))
