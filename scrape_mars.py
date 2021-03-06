#!/usr/bin/env python
# coding: utf-8


#Dependencies
import os
from bs4 import BeautifulSoup as soup
import requests
from splinter import Browser
import pandas as pd


def init_browser():
    # Initiate driver for deployment
    executable_path = {'executable_path': 'C:\\bin\\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless = True)

def scrape():
    browser = init_browser()

    news_title, news_paragraph = mars_news()

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(),
        "facts": mars_facts(),
        "hemispheres": hemispheres()
    }

    #Stop webdriver and return data
    browser.quit()
    return data


#Get Mars News
def mars_news():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

    # Convert the browser html to a soup object and then extract title and teaser paragraph
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')
    news_title = slide_elem.find('div',class_ = "content_title").get_text()
    news_p = slide_elem.find('div',class_ = "article_teaser_body").get_text()

    #Add news info to data dictionary
    return news_title, news_p

    browser.quit()


# Get Featured Image
def featured_image():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.is_element_present_by_id('full_image', wait_time=1)

    #Visit page by Splinter
    browser.click_link_by_id('full_image')
    browser.click_link_by_partial_text('more info')

    #Get featured image url
    fig = browser.find_by_tag('figure')
    img = fig.find_by_tag('img')
    for x in img:
        featured_image_url = x["src"]
    
    #Add featured image url to data dictionary
    browser.quit()
    return featured_image_url

    


# Get Mars Facts
def mars_facts():
    browser = init_browser()
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    #Use Pandas to scrape the page for table
    tables = pd.read_html(url)
    df = tables[0]
    #Add column headings
    df.columns = ['Description', 'Mars']
    #Convert to HTML table
    html_table = df.to_html()

    #Add table to data dictionary
    browser.quit()
    return html_table


# Mars Hemishperes
def hemispheres():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #Use Splinter to pull hemisphere image url and title
    links = browser.links.find_by_partial_text('Hemisphere')
    
    #Create a dictionary to hold title and image urls

    hemisphere_image_urls = []

    for i in range(len(links)):
        dic = {}
        
        #Find the elements on each iteration
        browser.find_by_css("a.product-item h3")[i].click()

        #Find the Sample image anchor tag and extract the href and append the URL to url array
        sample = browser.find_link_by_text('Sample').first
        dic["img_url"] = sample['href']
        content = browser.find_by_css ("h2.title")
        dic["title"] = content.text
        hemisphere_image_urls.append(dic)
        
        #Navigate backwards
        browser.back()
        
    #add Hemisphere title and image url to data dictionary
    browser.quit()
    return hemisphere_image_urls





