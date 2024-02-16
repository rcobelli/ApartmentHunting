from datetime import datetime
import time
from bs4 import BeautifulSoup
from Apartment import Apartment
from Option import Option
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List

class Paradigm(Apartment):
    def parseWebsite(self, url, building) -> List[Option]:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        apts = soup.find_all("div", {"class": "inner-card-container"})

        output = []

        for apt in apts:
            date = apt.find("span", {"class": "availability"}).text.replace("Available ", "")
            if "Unit" in date:
                date = datetime.today()
            else:
                date = datetime.strptime(date.strip(), '%b %d, %Y')

            sqFt = int(apt.find("span", {"class": "dynamic-text-after"}).text.replace("sq. ft", "").replace("+\xa0\n", "").replace(",", ""))
            beds = apt.find("span", {"class": "dynamic-text-before"}).text.split()[0]
            price = apt.find("span", {"class": "small-text"}).text.replace("Starting from ", "").replace("per month", "")
            withDen = "with den" if ("Den" in apt.text) else ""
            term = "TBD"
            id = apt.find("h2", {"class": "fp-title"}).text.replace("The", "")

            output.append(Option(building, id, price, date, sqFt, beds, withDen, term))

        return output
    
class MeridianCourthouse(Paradigm):
    def getPrice(self):
        return super().parseWebsite("https://www.meridiancourthouse.com/arlington/meridian-at-courthouse-commons/conventional/", "Meridian at Courthouse")
    
class MeridianBallston(Paradigm):
    def getPrice(self):
        return super().parseWebsite("https://www.meridianballston.com/arlington-va-apartments/meridian-at-ballston-commons-meridianballstoncommons/conventional/", "Meridian at Ballston")