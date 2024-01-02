import os
import sys
from dotenv import load_dotenv
from datetime import timedelta
import datetime as dt

import app

## argv
## mac : 0
## mac arm : 1
## linux : 2


def getDate() : 
    now = dt.datetime.today()
    today = now.strftime("%-m월%-d일")
    return today
        

if __name__ == "__main__":  
    date1 = getDate()
    
    # date1 = "01월02일"
    print("@@@@@@@@@@@@@")
    print(date1)
    
    load_dotenv(verbose=True)
    slackToken = os.getenv("TEST_TOKEN")
    channel = os.getenv("TEST_CHANNEL")
    app.app(slackToken, channel, date1)
   
