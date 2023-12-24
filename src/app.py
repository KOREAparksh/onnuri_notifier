import sys
import os

import crawling
import slack

def app(slackToken, channel, date):
     # 매개변수 확인
    if  len(sys.argv) != 3:
        slack.sendSlackErrorMessage("매개변수 문제로 프로그램이 종료되었습니다.(Not found argument)", slackToken , channel)
        print("매개변수는 os환경 별 숫자(0: mac, 1: mac arm, 2: linux)와 이미지저장경로를 입력해주세요.")
        sys.exit()
    
    # 블로그 홈에서 오늘 포스트의 url을 가져옴
    hrefValue = crawling.getTodayPostUrl(date)
    if hrefValue == None:
        slack.sendSlackErrorMessage("오늘 포스트가 올라오지 않은 것 같아요. 홈페이지를 확인하세요", slackToken , channel)
        sys.exit()
    
    # 블로그에서 게시글 내 이미지들의 url을 가져옴
    imageUrls = crawling.getImageUrls(hrefValue)
    print("imageurls: ", imageUrls)
    if (imageUrls == None):
        slack.sendSlackErrorMessage("홈페이지에서 메뉴 이미지를 불러오지 못했습니다.", slackToken , channel)
        sys.exit()
    
    slack.sendSlackLaunchMessage(imageUrls, slackToken, channel)

