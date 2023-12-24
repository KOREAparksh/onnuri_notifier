from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import os

def getImageUrls() :
    try :
        url = os.getenv("CRAWLING_URL")

        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        
        imageUrlList = []

        bidUrl = soup.find_all("div", attrs = {"class" : "se-component se-image se-l-default"})
        for div in bidUrl:
            imageUrl = div.find("img")["src"].split('?')
            imageUrlList.append(imageUrl[0] + "?type=w773")
        
        return imageUrlList
    except AttributeError :
        return None

def getTodayMenuImage():
    print()
