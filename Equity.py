from datetime import datetime
from bs4 import BeautifulSoup
from Apartment import Apartment
from Option import Option
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import List
import re
import hashlib

class Equity(Apartment):
    def parseWebsite(self, url, building) -> List[Option]:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        try:
            # Selenium doesn't think we can click it, so we do so anyways
            python_button = driver.find_element(By.CLASS_NAME, 'more-available')
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(python_button, 0, 0)
            action.click()
            action.perform()
        except:
            pass

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        apts = soup.find_all("div", {"class": "specs"})

        output = []
        datePattern = re.compile(r'\d{1,2}\/\d{1,2}\/\d{4}')
        sqFtPattern = re.compile(r'\d*,*\d{3,4} sq. ft.')
        bedsPattern = re.compile(r'\d Bed')

        for apt in apts:
            date = datetime.strptime(re.findall(datePattern, apt.text)[0], '%m/%d/%Y')
            sqFt = int(re.findall(sqFtPattern, apt.text)[0].split()[0].replace(",", ""))
            beds = re.findall(bedsPattern, apt.text)[0].split()[0]
            term = "12 mo. lease"
            price = apt.find("span", {"class": "pricing"}).text
            id = str(int(hashlib.sha1(apt.find("p", {"class": "description"}, 'utf-8').text.encode("utf-8")).hexdigest(), 16) % (10 ** 8))

            output.append(Option(building, id, price, date, sqFt, beds, "", term))

        return output
    
class TheClarendon(Equity):
    def getPrice(self):
        return super().parseWebsite("https://www.equityapartments.com/arlington/clarendon/the-clarendon-apartments", "The Clarendon")
    
class Wilson2201(Equity):
    def getPrice(self):
        return super().parseWebsite("https://www.equityapartments.com/arlington/courthouse/2201-wilson-apartments", "2201 Wilson")
    
class CourthousePlaza(Equity):
    def getPrice(self):
        return super().parseWebsite("https://www.equityapartments.com/arlington/courthouse/courthouse-plaza-apartments", "Courthouse Plaza")
    
class LibertyTower(Equity):
    def getPrice(self):
        return super().parseWebsite("https://www.equityapartments.com/arlington/ballston/liberty-tower-apartments", "Liberty Tower")
    
class Oak1800(Equity):
    def getPrice(self):
        return super().parseWebsite("https://www.equityapartments.com/arlington/rosslyn/1800-oak-apartments", "1800 Oak")
    
class ThePrime(Equity):
    def getPrice(self):
        return super().parseWebsite("https://www.equityapartments.com/arlington/courthouse/the-prime-at-arlington-courthouse-apartments", "The Prime")
    
class ReserveAtClarendon(Equity):
    def getPrice(self):
        return super().parseWebsite("https://www.equityapartments.com/arlington/clarendon/the-reserve-at-clarendon-centre-apartments", "Reserve at Clarendon")