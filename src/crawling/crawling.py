from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initOptions() :
    # 옵션 생성
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    
    return options

def initBrowser():
    options =  initOptions()
    
    nowPath = os.path.dirname(os.path.realpath(__file__))
    osEnvironment = sys.argv[1]
    
    
    if sys.argv[1] == '0':
        path = nowPath + "/chromedriver_mac"
        browser = webdriver.Chrome(service=Service(executable_path=path), options=options)
    if sys.argv[1] == '1':
        path = nowPath + "/chromedriver_mac_arm"
        browser = webdriver.Chrome(service=Service(executable_path=path), options=options)
    if sys.argv[1] == '2':
        path = nowPath + "/chromedriver_linux"
        browser = webdriver.Chrome(service=Service(executable_path=path), options=options)
    return browser

def getFirstATagHrefValue(today):
    url = os.getenv("CRAWLING_URL")
    driver = initBrowser()
    driver.get(url)
    hrefValue = None
    flag = True
    print("11111111111")
    try:
        # firstATags = driver.find_elements(By.XPATH, '//div[@class="text_area___UrFH"]')
        wait = WebDriverWait(driver, 20)
        print("22222222222222")
        divs = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="text_area__mOuKZ"]')))
        print("33333333333333")
        print("divs: ", type(divs))
        for div in divs:
            title = div.find_element(By.XPATH, '//strong[1]')
            title = div.text
            title = title.replace(" ", "")
            title = title.strip()
            print("타이틀 값:", title)
            if (title.find(today+"오늘의점심") == -1):
                continue
            flag = False
            aTag = div.find_element(By.TAG_NAME, 'a')
            print("첫 번째 a 태그의 href 속성 값:", aTag.get_attribute("href"))
            hrefValue = aTag.get_attribute("href")
            break
        if (flag == True):
            print("오늘 포스트가 없습니다.")
            raise Exception("오늘 포스트가 없습니다.") 
    except Exception as e:
        print("error: ", e)
    finally:
        driver.close()
    return hrefValue

# ===============================================================================================
# ===============================================================================================
# ===============================================================================================
# ===============================================================================================
# ===============================================================================================
# ===============================================================================================
# ===============================================================================================


def getTodayPostUrl(today) :
    hrefValue = getFirstATagHrefValue(today)
    if (hrefValue == None):
        print("온누리 홈페이지에서 a 태그의 href 속성 값을 가져오지 못했습니다.")
        return None
    return hrefValue
    

def getImageUrls(hrefValue) :
    try :
        url = hrefValue
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        
        imageUrlList = []
        bidUrl = soup.find_all("div", attrs = {"class" : "se-component se-image se-l-default"})
        for div in bidUrl:
            imageUrl = div.find("img")["src"].split('?')
            imageUrlList.append(imageUrl[0] + "?type=w800")
        return imageUrlList
    except AttributeError :
        return None



# strong 태그 직접 찾는법
# wait = WebDriverWait(driver, 20)
# firstATag = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="contentslist_block"]//a[1]')))
# titleText = driver.find_element(By.XPATH,'//div[@id="contentslist_block"]//strong[1]')

# titleText = titleText.replace(" ", "")
# titleText = titleText.strip()
# print("타이틀 텍스트:", titleText)
# if (titleText.find(today) == -1):
#     print("오늘 포스트가 아닙니다.")
#     raise Exception("오늘 포스트가 아닙니다.") 

# AWS에서 실행되는지 보면 됨 그리고 회사 슬랙에 설치