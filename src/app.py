import sys
import os

import crawling
import imageParser
import slack

def app(slackToken, channel, date1, date2):
     # 매개변수 확인
    if len(sys.argv) != 2:
        slack.sendSlackErrorMessage("매개변수 문제로 프로그램이 종료되었습니다.(Not found argument)", slackToken , channel)
        print("매개변수 하나 지정해서 넣으소")
        sys.exit()
        
    menuTimeFlag = sys.argv[1]
    
    if (menuTimeFlag != '0' and menuTimeFlag != '1' and menuTimeFlag != '2')  :
        slack.sendSlackErrorMessage("매개변수 문제로 프로그램이 종료되었습니다. (Invalid argument)", slackToken , channel)
        print("매개변수 0, 1, 2 중에 넣으소")
        sys.exit()
    isLaunch = sys.argv[1] == '0'


    # 블로그에서 게시글 내 이미지들의 url을 가져옴
    imageUrlList = crawling.getImageUrls()
    if (imageUrlList == None):
        slack.sendSlackErrorMessage("홈페이지에서 메뉴 이미지를 불러오지 못했습니다.", slackToken , channel)
        print("조졌네이~")
        sys.exit()
    
    # 마지막 이미지는 건물 소개 이미지라 삭제하였음
    imageUrlList.pop() 
    
    # OCR 돌린 결과를 {date : url} 로 가져옴 
    imageMap = imageParser.findImages(imageUrlList)
    keyList = list(imageMap.keys())
    foundImageUrls = []

    print("???")
    print(keyList)
    if sys.argv[1] == '0':
        for key in keyList:
            if ("점심" in key and date1 in key):
                foundImageUrls.append(imageMap[key])
        if (len(foundImageUrls) != 1):
            slack.sendSlackErrorMessage("해당 날짜의 이미지를 찾지 못했습니다.", slackToken , channel)
            
        slack.sendSlackLaunchMessage(foundImageUrls[0], slackToken, channel)

    elif sys.argv[1] == '1':
        for key in keyList:
            print(key)
            if (("저녁" in key and date1 in key) or ("점심" in key and date2 in key)):
                foundImageUrls.append(imageMap[key])
        if (len(foundImageUrls) != 2):
            slack.sendSlackErrorMessage("해당 날짜의 이미지를 찾지 못했습니다. - 2개의 이미지를 찾지 못함", slackToken , channel)
        
        slack.sendSlackDinnerMessage(foundImageUrls[0], foundImageUrls[1], slackToken, channel)

    elif sys.argv[1] == '2':
        for key in keyList:
            if ("점심" in key and date1 in key):
                foundImageUrls.append(imageMap[key])
        if (len(foundImageUrls) != 1):
            slack.sendSlackErrorMessage("해당 날짜의 이미지를 찾지 못했습니다.", slackToken , channel)
            
        slack.sendSlackFridayMessage(foundImageUrls[0], slackToken, channel)

    