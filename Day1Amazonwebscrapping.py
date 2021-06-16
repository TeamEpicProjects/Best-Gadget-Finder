from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

s = HTMLSession()
searchterm = 'mobile'
url = f'https://www.amazon.in/s?k={searchterm}&ref=nb_sb_noss'

def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html,'html.parser')
    return soup

def getproducts(soup):
    products = soup.find_all('div', {'data-component-type':'s-search-result'})
    for item in products:
        Productname = item.find('a',{'class':'a-link-normal a-text-normal'}).text.strip()
        print(Productname)
        salesPrice = item.find_all('span',{'class':'a-price-whole'})[0].text.strip()
        print(salesPrice)
        oldPrice = item.find_all('span', {'class': 'a-offscreen'})[1].text.strip()
        print(oldPrice)
        reviewvalue = item.find('Span', {'class':'a-icon-alt'})
        print(reviewvalue)
        reviewno = item.find('Span', {'class': 'a-size-base'})
        print(reviewno)


soup = getdata(url)
getproducts(soup)
