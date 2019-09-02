from bs4 import BeautifulSoup
import urllib.request
import time
from requests import get
import urlopen
import re
import time
import csv
import xlsxwriter

car_data = []
def scrape():
    for page in range(1, 2):

        source = urllib.request.urlopen(
            'https://www.autotrader.co.uk/car-search?onesearchad=New&advertising-location=at_cars&newCarHasDeal=on&postcode=ec1a4eu&sort=distance&radius=1500&page={}'.format(
                page))
        soup = BeautifulSoup(source, 'html.parser')
        cars = soup.findAll('li', attrs={'class': 'search-page__result'})

        print("Details of the page : {} ".format(page))

        for car in cars:
            car_details = car.find('div', attrs={'class': 'information-container'})
            car_name = (car_details.find('h2', attrs={'class', 'listing-title title-wrap'}).get_text()).strip("\n")
            extra_details = car_details.find('ul', attrs={'class', 'listing-extra-detail'}).get_text()
            details = re.sub(r'BRAND NEW - ', "", extra_details).strip("\n")
            image = car.find('img', attrs={'src': re.compile('.jpg')})
            car_image = (image['src'])

            prices = car.find('section', attrs={'class': 'price-column'})
            mrp = prices.find('div', attrs={'class', 'physical-stock-mrrp'}).get_text() if prices.find('div',
                                                                                                       attrs={'class',
                                                                                                              'physical-stock-mrrp'}) else ''
            max_price = re.sub(r'RRP\n', "", mrp).strip("\n")
            price = (prices.find('div', attrs={'class', 'physical-stock-now'}).get_text()).strip("\n") if prices.find(
                'div', attrs={'class', 'physical-stock-now'}) else ''
            href = car_details.find('h2', attrs={'class', 'listing-title title-wrap'}).find("a", href=True)
            key_specs = car_details.find('ul', attrs={'class': 'listing-key-specs'}).findAll('li')

            type = key_specs[0].get_text() if key_specs[0] else ''
            e_type = key_specs[1].get_text() if key_specs[1] else ''
            engine = key_specs[2].get_text() if key_specs[2] else ''
            transmission = key_specs[3].get_text() if key_specs[3] else ''
            f_type = key_specs[4].get_text() if key_specs[4] else 'Null'

            dictionary = {
                "Car Name": car_name,
                "MRP-Price": max_price,
                "Actual Price": price,
                "Availability": details,
                "Url": href['href'],
                "Image": car_image,
                "Type": type,
                "Engine Power": engine,
                "Engine Model": e_type,
                "Car Transmission": transmission,
                "Fuel Type": f_type
            }

            car_data.append(dictionary)

        time.sleep(1)

    return car_data


def export_to_csv(car_data):
   fp = open('new_car_details.csv', 'w')
   with fp:
       for k, v in enumerate(car_data):
           header_fields = v.keys()
           writer = csv.DictWriter(fp, fieldnames=header_fields)
           writer.writeheader()
       writer.writerow(v)
       print("csv complete")

def export_to_xls(car_data):
    workbook = xlsxwriter.Workbook('car_details.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    for key, car_details in enumerate(car_data):
        headers = car_details.keys()

        if row == 0:
            head_col = 0
            for header_name in headers:
                worksheet.write(row, head_col, header_name)
                head_col = head_col + 1
            row += 1

        col = 0
        for name, value in car_details.items():
            worksheet.write(row, col, value)
            col = col + 1
        row += 1

    workbook.close()
    print("xls complete!")


def updater():
    start_time = time.time()


car_data = scrape()
export_to_xls(car_data)
export_to_csv(car_data)

