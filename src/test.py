import os
import sys
from dotenv import load_dotenv
from datetime import timedelta
import datetime as dt

import app

## argv
## 점심 : 0
## 저녁 : 1
## 금요일저녁 : 2

def getDate(argv) : 
    if sys.argv[1] == '0':
        now = dt.datetime.today()
        today = now.strftime("%m월%d일")
        return today, ""
        
    if sys.argv[1] == '1':
        now = dt.datetime.today()
        today = now.strftime("%m월%d일")
        now = now + dt.timedelta(days=1)
        tomorrow = now.strftime("%m월%d일")
        return today, tomorrow
    
    if sys.argv[1] == '2':
        now = dt.datetime.today() + dt.timedelta(days=3)
        today = now.strftime("%m월%d일")
        return today, ""
        

if __name__ == "__main__":  
    date1, date2 = getDate(sys.argv[1])
    
    date1 = "08월28일"
    date2 = "08월28일"
    print("@@@@@@@@@@@@@")
    print(date1)
    print(date2)
    print(date2 == '')
    
    load_dotenv(verbose=True)
    slackToken = os.getenv("TEST_TOKEN")
    channel = os.getenv("TEST_CHANNEL")
    app.app(slackToken, channel, date1, date2)
   
