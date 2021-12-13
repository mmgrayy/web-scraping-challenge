# Dependencies
from bs4.element import ProcessingInstruction
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

def init_browser():
    executable_path = {'executable_path':'/Users/meredithgray/Downloads/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)
def scrape():
    browser = init_browser()
    mars_dict ={}
    # Mars News URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #  news title
    news_title=soup.find('div',class_= 'content_title').text
    #  news paragraph
    news_p=soup.find('div', class_= 'article_teaser_body').text
    
    
    # Visit the JPL Mars URL
    # URL for the featured space image site
    featured_url = "https://spaceimages-mars.com/"
    browser.visit(featured_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    featured_html = browser.html
    featured_soup = BeautifulSoup(featured_html, 'html.parser')
    featured_image = featured_soup.find_all(
        'img', class_='headerimage fade-in')[0]["src"]
    featured_image_url = featured_url + featured_image


    
    ## Scrape Mars facts
    url='https://galaxyfacts-mars.com/'
    tables=pd.read_html(url)
    mars_fact=tables[0]
    mars_fact.columns = ['Description','Value','Value']
    mars_fact_table=mars_fact.to_html()
    mars_fact_table.replace('\n','') 
    
   # URL to get the high resolution images
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)



    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')

    hemisphere = hemisphere_soup.find('div', class_='collapsible results')

    all_hemispheres = hemisphere.find_all('div', class_='item')

    images_titles = []

    for individual in all_hemispheres:
        img_title = individual.find('h3').text
        img_title = img_title.replace("Enhanced", "")

        image_url = individual.find('img', class_='thumb')['src']
        image_src = hemisphere_url + image_url
    # Define the hemispehere dictionary and set the values
        hemisphere_dict = {}
        hemisphere_dict["title"] = img_title
        hemisphere_dict["img_src"] = image_src

        images_titles.append(hemisphere_dict)


    # Mars 
    mars_dict= {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_fact_table),
        "hemisphere_images": images_titles
    }
    
    
    #print(mars_dict)

    
    return mars_dict

#my_function= scrape()