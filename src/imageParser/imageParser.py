import os
from dotenv import load_dotenv
import pytesseract
import cv2 
import datetime as dt
import uuid
import time
import json
import requests


def getCropedImage(url):
    today = dt.datetime.today()
    today = today.strftime("%m월%d일%H시%M분%S초%f")

    initFileName = "./image/init" + today + ".png"
    cropFileName = "./image/crop" + today + ".png"
    
    print(initFileName)
    os.system("mkdir -p image")
    os.system("curl " + url + " > " + initFileName)
    img = cv2.imread(initFileName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # gray = cv2.medianBlur(gray, 5)
    # cv2.imwrite('./image/grayImage.png',gray)
    
    cropGray = gray[80:190,180:800]
    cv2.imwrite(cropFileName,cropGray)
    os.system("rm -rf ./image")
    return cropGray



def imageToString(image):
    text = pytesseract.image_to_string(image, lang='Hangul', config = '-l Hangul --oem 3 --psm 6')
    text = text.replace(" ", "")
    return text


def getText(url):
    api_url = os.getenv("NAVER_API_URL")
    secret_key = os.getenv("NAVER_SECRET_KEY")
    
    request_json = {
        'images': [
            {
                'format': 'jpeg',
                'name': 'demo',
                'url' : url
            }
        ],
        'requestId': str(uuid.uuid4()),
        'lang' : "ko",
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }
    
    headers = {
    'X-OCR-SECRET': secret_key,
    'Content-Type' : 'application/json'
    }
    
    response = requests.request("POST", api_url, headers=headers, data = json.dumps(request_json).encode('UTF-8'))
    
    if response.status_code != 200 :
        return "temp"
    
    text = ""
    result = json.loads(response.text)
    images = result['images']
    fields = images[0]['fields']
    for data in fields:
        inferText = data['inferText']
        inferText = inferText.replace(" " , "")
        text += inferText
    return text
    

def findImages(imageUrlList):
    urlDictionary = {}

    for url in imageUrlList:
        # cropedImage = getCropedImage(url)
        # text = imageToString(cropedImage)
        text = getText(url)
        text = text.strip()
        urlDictionary[text] = url
        
    return urlDictionary