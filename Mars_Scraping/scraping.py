
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# Set up function to initiate browser, create data dictionary and end webdriver while returning scraped data
def scrape_all():
    # Set up executable path/Splinter / Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_p = mars_news(browser)


    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object 
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title' 
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

# Define and declare function
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ### Mars Facts


# Add function
def mars_facts():

    # Add try/except for error handling
    try:
        # Scrape entire facts table using Pandas .read_html()
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert df back to html
    return df.to_html()


# ### Hemisphere Images


# Add Function
def hemispheres(browser):

    # Visit the mars hemispheres site
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the html
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # scrape all items for hemispheres
    items = hemi_soup.find_all('div', class_='item')

    for i in items:
        # Create empty hemispheres dictionary
        hemispheres = {}
        # scrape the titles
        titles = i.find('h3').text
        # link for high resolution full size image
        fs_link = i.find('a', class_='itemLink product-item').get('href')
        # create absolute url with base url
        abs_url = f'https://marshemispheres.com/{fs_link}'
        # visit absolute url
        browser.visit(abs_url)
        # parse resulting html with soup
        fs_img_html = browser.html
        img_soup = soup(fs_img_html, 'html.parser')
        original = img_soup.find('div', class_='downloads')
        img_url = (abs_url + (original.find('a').get('href')))
    
        # add/append to hemisphere_image_urls list
        hemispheres["img_url"] = img_url
        hemispheres["title"] = titles
        hemisphere_image_urls.append(hemispheres)
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":
     # If running as script, print scraped data
    print(scrape_all())
