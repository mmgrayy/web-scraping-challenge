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

    
    ## Scrape Mars facts
    url='https://galaxyfacts-mars.com/'
    tables=pd.read_html(url)
    mars_fact=tables[0]
    mars_fact.columns = ['Description','Value','Value']
    mars_fact_table=mars_fact.to_html()
    mars_fact_table.replace('\n','') 
    
    # Scrape Mars hemisphere title and image
    hemisphere_url='https://marshemispheres.com/'
    browser.visit(hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    all_mars_hemispheres = soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []
    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(hemisphere_url + hemisphere_link)
        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(image_dict)


    # Mars 
    mars_dict= {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_fact_table),
        "hemisphere_images": hemisphere_image_urls
    }
    
    
    #print(mars_dict)

    
    return mars_dict

#my_function= scrape()