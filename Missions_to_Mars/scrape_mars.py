# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import time
from selenium import webdriver

#Setup splinter
def init_browser():
    executable_path = {'executable_path':'/Users/meredithgray/Downloads/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

    #1 

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest news title
    news_title=soup.find('div', class_= 'content_title').text
    # Retrieve the latest news paragraph
    news_p=soup.find('div', class_= 'article_teaser_body').text
    #Add items into the mars_data dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p



    # Visit the JPL Mars URL
    url= 'https://spaceimages-mars.com'
    jpl_image_url= 'https://spaceimages-mars.com/image/featured/mars3.jpg'
    browser.visit(url)  
    # Scrape the browser into soup and use soup to find the image of mars
    # Save the image url to a variable called `img_url`
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find("img", class_="headerimage fade-in")["src"]
    img_url = "https://spaceimages-mars.com"+image
    featured_image_url = img_url
    #Add item to mars_data dictionary
    mars_data['featured_image_url'] = featured_image_url

    # Scrape Mars facts
    url='https://galaxyfacts-mars.com/'
    tables=pd.read_html(url)
    mars_fact=tables[0]
    mars_fact.columns = ['Description','Value','Value']
    mars_fact_table=mars_fact.to_html()
    mars_fact_table.replace('\n','')
    mars_data['mars_fact_table'] = mars_fact_table


# # Mars Hemispheres

# Scrape Mars hemisphere title and image
    # Scrape Mars hemisphere title and image
    hemisphere_url='https://marshemispheres.com/'
    browser.visit(hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')   
    # Mars hemispheres products data
    all_mars_hemispheres = soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []
    
    
        hemisphere_info = {}
   
   for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url        
        hemisphere_image_urls.append(image_dict)