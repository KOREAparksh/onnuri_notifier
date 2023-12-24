import os
import sys
from dotenv import load_dotenv
from datetime import timedelta
import datetime as dt

import app

def getDate(argv) : 
    now = dt.datetime.today()
    today = now.strftime("%m월%d일")

if __name__ == "__main__":  
    date1 = getDate()
    
    load_dotenv(verbose=True)
    slackToken = os.getenv("SLACK_TOKEN")
    channel = os.getenv("SLACK_CHANNEL")
    app.app(slackToken, channel, date1, date2)
   
