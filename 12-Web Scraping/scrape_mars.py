# Import Dependecies 
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd

# Initialize browser
def init_browser(): 
    # Excutable path to driver
    executable_path = {"executable_path": os.path.join("C:\\", "projects", "chromedriver_win32", "chromedriver.exe")}
    browser =  Browser("chrome", **executable_path, headless=True)
    return browser 

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# MARS NEWS
def scrape_mars_news(browser):
    try: 

        # Initialize browser 
        browser = init_browser()

        # HTML Object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        
        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p


        return mars_info

    finally:

        browser.quit()

# FEATURED IMAGE
def scrape_JPL_mars_image(browser):

    try: 

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("img.jpg", wait_time=1)

        # Visit Mars Space Images through splinter module
        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image_url)

        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')

        # Find image
        image = soup.find("img", class_="thumb")["src"]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        featured_image_url = main_url + image

        # Display full link to featured image
        featured_image_url 

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    finally:

        browser.quit()

        

# Mars Weather 
def scrape_mars_weather(browser):

    try: 

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("div", wait_time=1)

        # Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object 
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find all elements that contain tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Retrieve all elements that contain news title in the specified range
        # Look for entries that display weather related words to exclude non weather related tweets 
        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'InSight' and 'winds' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

        # Dictionary entry from WEATHER TWEET
        mars_info['weather_tweet'] = weather_tweet
        
        return mars_info
    finally:

        browser.quit()


# Mars Facts
def scrape_mars_facts(browser):

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = data

    return mars_info


# MARS HEMISPHERES
def scrape_mars_hemispheres(browser):

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemisphere_image_urls = []

        # Store the main_ul 
        main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for item in items: 

            # Store link that leads to full image website
            image_path = item.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(main_url + image_path)
            
            # HTML Object of individual hemisphere information website 
            inv_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup(inv_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

            # Store title
            title = item.find('h3').text

        mars_info['hemisphere_image_urls'] = hemisphere_image_urls

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()