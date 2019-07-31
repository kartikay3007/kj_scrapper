import bs4 as bs
from bs4 import BeautifulSoup
import urllib.request
import time
from requests import get
import urllib3.response, urlopen
from urllib3 import *
import socket
import urlopen
from urllib.parse import urlparse, urlsplit
import os
import re
import link


def scrape():

    source = urllib.request.urlopen('https://www.autotrader.co.uk/car-search?onesearchad=New&advertising-location=at_cars&newCarHasDeal=on&postcode=ec1a4eu&sort=distance&radius=1500')


    soup = bs.BeautifulSoup(source, 'html.parser')



    cars = soup.findAll('li', attrs={'class': 'search-page__result'})


    #car_data = []
    print("Details of the car to read:")
    for car in cars:
        car_details = car.find('div', attrs={'class': 'information-container'})
        car_name = (car_details.find('h2', attrs={'class', 'listing-title title-wrap'}).get_text()).strip("\n")
        extra_details = car_details.find('ul', attrs={'class', 'listing-extra-detail'}).get_text()
        details = re.sub(r'BRAND NEW - ',"", extra_details).strip("\n")
        image = car.find('img', attrs={'src' : re.compile('.jpg')})
        car_image = (image['src'])

        prices = car.find('section', attrs={'class': 'price-column'})
        mrp = prices.find('div', attrs={'class', 'physical-stock-mrrp'}).get_text()if prices.find('div', attrs={'class', 'physical-stock-mrrp'}) else ''
        max_price = re.sub(r'RRP\n', "", mrp).strip("\n")
        price = (prices.find('div', attrs={'class', 'physical-stock-now'}).get_text()).strip("\n") if prices.find('div', attrs={'class', 'physical-stock-now'}) else ''

        href = car_details.find('h2', attrs={'class', 'listing-title title-wrap'}).find("a", href=True)

        key_specs = car_details.find('ul', attrs={'class': 'listing-key-specs'}).findAll('li')


        type = key_specs[0].get_text() if key_specs[0] else ''
        e_type = key_specs[1].get_text() if key_specs[1] else ''
        engine = key_specs[2].get_text() if key_specs[2] else ''
        transmission = key_specs[3].get_text() if key_specs[3] else ''
        f_type = key_specs[4].get_text() if key_specs[4] else ''



        dictionary = {
                      "Car Name": car_name,
                      "MRP-Price": max_price,
                      "Actual Price": price,
                      "Availability": details,
                      "Url": href['href'],
                      "Image": car_image,
                      "Type": type,
                      "Engine_Power": engine,
                      "Engine_Model": e_type,
                      "Car Transmission": transmission,
                      "Fuel_Type": f_type
                      }

        #car_data.append(dictionary)
        car_data = [(k, v) for k, v in dictionary.items()]
        print(car_data)




def updater():
    start_time = time.time()
    scrape()





updater()
