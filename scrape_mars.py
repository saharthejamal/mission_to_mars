from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo


# DB Setup
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

# NASA Mars News
def marsnews():
    mars_url = 'https://www.redplanetscience.com'
    browser.visit(mars_url)
    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')
    news_title = news_soup.find('div', class_='content_title').text
    news_p = news_soup.find('div', class_="article_teaser_body").text
    news = [news_title, news_p]
    return news

# JPL Mars Space Featured Image
def marsimage():
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')
    fi_url_rel = jpl_soup.find('img', class_="headerimage", src = True)['src']
    fi_url = jpl_url + fi_url_rel
    print(fi_url)
    fi_name = jpl_soup.find('h1', class_='media_feature_title').text
    fi = [fi_url, fi_name]
    return fi

# Mars Facts
def marsfacts():
    facts_url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(facts_url)
    mars_table = tables[1]
    mars_table.columns = ["Dimension", "Value"]
    mars_table.set_index("Dimension", inplace= True)
    mars_table_html =  mars_table.to_html()
    return mars_table_html

# Mars Hemispheres
def marshemi():
    main_url = 'https://marshemispheres.com/'
    browser.visit(main_url)
    main_html = browser.html
    main_soup = bs(main_html, 'html.parser')
    links = []
    names = []
    results = main_soup.find_all('div', class_='description')
    for result in results:
        h3 = result.find('h3').text
        href = result.find('a')['href']
        link = main_url + href
        links.append(link)
        names.append(h3)
    img_links = []
    for link in links:
        url = link
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')

        img = soup.find('img', class_="wide-image")['src']
        img_link = main_url+img
        img_links.append(img_link)
    df = pd.DataFrame(
        {
        'title': names,
        'img_url': img_links
        }
    )
    hemisphere_image_urls = df.to_dict('records')
    return hemisphere_image_urls

# Set up scrape and dictionary
def scrape():
    final_data= dict()
    news = marsnews()
    fi = marsimage()
    final_data["news_title"] = news[0]
    final_data["news_para"] = news[1]
    final_data["fi_img"] = fi[0]
    final_data["fi_title"] = fi[1]
    final_data["facts"] = marsfacts()
    final_data["hemispheres"] = marshemi()
    return final_data

test = scrape()
print(test)