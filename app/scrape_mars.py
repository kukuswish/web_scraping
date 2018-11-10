# Dependencies
import pandas as pd
import json
import datetime
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrapeData():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = webdriver.Chrome("./chromedriver")

    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)

    browser.get(url)
    soup = BeautifulSoup(browser.page_source,"html.parser")

    #get page
    pg= soup.find("div", {"id": "page"})

    #get the item list
    #get first child ** lastest news ** 

    items= pg.find('ul', class_="item_list ")
    first_child = items.findChild()

    latest_title = first_child.find('div', class_='content_title').text
    latest_teaser = first_child.find('div', class_='article_teaser_body').text

    #get featured image 
    fimage_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.get(fimage_url)
    soup = BeautifulSoup(browser.page_source,"html.parser")

    #get full image URL
    image_url = soup.find("a", {"id": "full_image"})['data-fancybox-href']
    image_url = 'https://www.jpl.nasa.gov' + image_url

    #twitter url
    twitterUrl = 'https://twitter.com/marswxreport?lang=en'
    browser.get(twitterUrl)
    soup = BeautifulSoup(browser.page_source,"html.parser")

    #get weather
    stream_items = soup.find('ol', class_="stream-items")
    stream_info = stream_items.findChild().find('div', class_='content').find('div',class_='js-tweet-text-container').find('p')

    weather = stream_info.text

    #get mars facts
    factUrl = 'https://space-facts.com/mars/'
    browser.get(factUrl)
    soup = BeautifulSoup(browser.page_source,"html.parser")

    factsTable=soup.find('table', {'id':'tablepress-mars'})
    facts=factsTable.find_all('tr')

    factsDF= pd.read_html(str(factsTable))

    factsDF=pd.DataFrame(factsDF[0])

    factsDF[0] = factsDF[0].map(lambda x: x.rstrip(':'))

    #hemispheres
    hmUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.get(hmUrl)
    soup = BeautifulSoup(browser.page_source,"html.parser")

    #go to links
    links= soup.find_all('div', class_='description')
    links

    images=[]

    for a in links:
        addlink=a.find('a')['href']
        newPage= 'https://astrogeology.usgs.gov' + addlink
        title=a.find('a').find('h3').text
        browser.get(newPage)
        sp = BeautifulSoup(browser.page_source,"html.parser")
        
        imageUrl=sp.find('img', class_='wide-image')['src']
        imageUrl='https://astrogeology.usgs.gov'+imageUrl
        images.append({'title':title, 'img_url': imageUrl})
        
    #all Data
    now = datetime.datetime.now()
    records = factsDF.to_json()
    dataSet = {
        'latestTitle': latest_title,
        'latestTeaser': latest_teaser,
        'featuredImage': image_url,
        'weather': weather,
        'facts': records,
        'hemispheres': images,
        'scrapedOn': now
    }
    browser.close()
    return dataSet;

