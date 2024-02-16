import time
from bs4 import BeautifulSoup
from Apartment import Apartment
from Option import Option
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List
import re

class Kettler(Apartment):
    def parseWebsite(self, url, building) -> List[Option]:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        apts = soup.find_all("div", {"class": "fp-container"})

        output = []
        sqFtPattern = re.compile(r'\d*,*\d{3,4} Sq. Ft.')
        bedsPattern = re.compile(r'\d Bed')
        pricePattern = re.compile(r'\$\d,\d{3}')

        for apt in apts:
            date = "TBD"
            sqFt = int(re.findall(sqFtPattern, apt.text)[0].split()[0].replace(",", ""))
            beds = re.findall(bedsPattern, apt.text)[0].split()[0]
            term = "12 mo. lease"
            price = re.findall(pricePattern, apt.text)[0]
            id = apt.find("h2", {"class": "card-title"}).text

            output.append(Option(building, id, price, date, sqFt, beds, "", term))

        return output
    
class GarfieldPark(Kettler):
    def getPrice(self):
        return super().parseWebsite("https://www.garfieldparkapts.com/floorplans", "Garfield Park")