import bs4
import requests
import csv
def scrape(perPage, page):
    #list of pages
    targets = []
    response = requests.get(f'https://www.scpper.com/pages/pageList?siteId=66711&deleted=0&page={page}&perPage={perPage}')
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
                            targets.append(a['href'])
    return(targets)
pages = []
for i in range(1, 15):
    targets = scrape(1000, i)
    pages = pages + targets
