import bs4
import requests
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
def scrape_pages(perPage, page):
    #list of pages
    pages = []
    print("Scraping page " + str(page))
    response = requests.get(f'https://www.scpper.com/pages/pageList?siteId=66711&deleted=0&page={page}&perPage={perPage}')
    print("Scraped page " + str(page))
    #get html from second json object
    soup = bs4.BeautifulSoup(response.json()['content'], 'html.parser')
    #for every div with responsive-table-row responsive-table-data class get the text
    for div in soup.find_all('div', class_='responsive-table-row responsive-table-data'):
        #for every div with responsive-table-cell pages-1 class get next div
        for div2 in div.find_all('div', class_='responsive-table-cell pages-1'):
            #for every div with responsive-table-column-group class get next div
            for div3 in div2.find_all('div', class_='responsive-table-column-group'):
                #for every div with responsive-table-cell pages-1-2 responsive-table-cell-data column-page class get next div
                for div4 in div3.find_all('div', class_='responsive-table-cell pages-1-2 responsive-table-cell-data column-page'):
                    #for every div with responsive-table-value responsive-table-value-default class get href
                    for div5 in div4.find_all('div', class_='responsive-table-value responsive-table-value-default'):
                        #for every a tag get href
                        for a in div5.find_all('a'):
                            pages.append(a['href'])
    return(pages)
def scrape_tags(page):
    #list of tags
    tags = []
    print("Scraping tags from, " + str(page))
    response = requests.get(f'https://www.scpper.com/pages/pageList?siteId=66711&deleted=0&page={page}&perPage=1')
    print("Scraped tags from " + str(page))
    #parsing html with bs4
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    #finding em tag
    for em in soup.find_all('em'):
        #for every a tag get text
        for a in em.find_all('a'):
            tags.append(a['href'])
    return(tags)
def get_pages(n, perPage, pagesNum):  #n - number of workers, perPage - number of links on one page, pagesNum - number of pages to scrape from, default: n=8, perPage=1000, pages = 15
    pages = []
    tasks = []
    with ThreadPoolExecutor(max_workers=n) as pool:
        for page in range(1, pagesNum+1):
            tasks.append(pool.submit(scrape_pages, perPage, page))
        for task in as_completed(tasks):
            pages = pages + task.result()
    return(pages)
def get_tags(n, pages):  #n - number of workers(default: 100), pages - list of pages to scrape from, e.g [/page/13241, /page/13242, ...]
    tags = []
    tasks = []
    with ThreadPoolExecutor(max_workers=n) as pool:
        for page in pages:
            tasks.append(pool.submit(scrape_tags, page))
        for task in as_completed(tasks):
            tags = tags + task.result()
    return(tags)
pages=get_pages(2, 10, 4)
print(pages)
tags=get_tags(2, pages)
print(tags)
