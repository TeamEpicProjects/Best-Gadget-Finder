from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

s = HTMLSession()
productList = []
searchterm = 'mobile'
url = f'https://www.amazon.in/s?k={searchterm}&ref=nb_sb_noss'

def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def getproducts(soup):
    products = soup.find_all('div', {'data-component-type':'s-search-result'})
    for item in products:

        Productname = item.find('span', {'class':'a-size-medium a-color-base a-text-normal'}).get_text()
       # print(Productname)

        try:
            salesPrice = item.find('span', {'class': 'a-price-whole'}).get_text()
        except:
            salesPrice = item.find('span', {'class': 'a-price-whole'})
     #   print(salesPrice)

        try:
            oldPrice = item.find('span', {'class': 'a-price a-text-price'}).find('span', {'class': 'a-offscreen'}).get_text()
        except:
            oldPrice = item.find('span', {'class': 'a-offscreen'})
      #  print(oldPrice)

        try:
            reviewvalue = item.find('span', {'class': 'a-icon-alt'}).get_text()
        except:
            reviewvalue = item.find('span', {'class': 'a-icon-alt'})
      #  print(reviewvalue)

        Link = item.find('a', {'class': 'a-link-normal a-text-normal'})
        productlink ='https://www.amazon.co.in' + str(Link['href'])
      #  print(productlink)
        image = item.find('img', {'class': 's-image'})
        imagelink=image['src']
      #  print(imagelink)

        Productdetails = {
            'Name': Productname,
            'SalesPrice': salesPrice,
            'OriginalPrice': oldPrice,
            'Reviews': reviewvalue,
            'ProductLink': productlink,
            'ImageLink': imagelink
        }
        productList.append(Productdetails)
    return

def getnextpage(soup) :
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url ='https://www.amazon.co.in' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return



while True:
    soup = getdata(url)
    getproducts(soup)
    url = getnextpage(soup)
    if not url:
        break
    else:
        print(url)

df = pd.DataFrame(productList)
df.to_csv('Productdata.csv', index=False)



