from datetime import datetime
import time
from bs4 import BeautifulSoup
from Apartment import Apartment
from Option import Option
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List
import re

class Bozzuto(Apartment):
    def parseWebsite(self, url, building) -> List[Option]:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        floorplans = soup.find_all("div", {"class": "floorplan-section"})

        output = []
        bedsPattern = re.compile(r'\d Bedroom')
        date = "TBD"
        term = "TBD"

        for floorplan in floorplans:
            beds = re.findall(bedsPattern, floorplan.find("div", {"class": "col-lg-8"}).text)[0].split()[0]

            apts = floorplan.find_all("tr", {"class": "unit-container"})
            for apt in apts:
                sqFt = int(apt.find("td", {"class": "td-card-sqft"}).text.replace("Sq. Ft.: ", "").replace(",", ""))

                if apt.find("td", {"class": "td-card-available"}) != None:
                    date = apt.find("td", {"class": "td-card-available"}).text.replace("Date:", "")
                    if "Available" in date:
                        date = datetime.today()
                    else:
                        date = datetime.strptime(date.strip(), '%m/%d/%Y')

                price = apt.find("td", {"class": "td-card-rent"}).text.split(" to ")[0].replace("Rent:", "")
                id = apt.find("td", {"class": "td-card-name"}).text.replace("Apartment:", "")

                amenities = apt.find("td", {"class": "td-card-details"})
                details = ""

                if amenities is not None:
                    if "Classic" in amenities.text:
                        details += "Classic "
                    elif "Standard" in amenities.text:
                        details += "Standard "
                    elif "Premium" in amenities.text:
                        details += "Premium "

                    if "Sunroom" in amenities.text:
                        details += "w/ sunroom"


                output.append(Option(building, id, price, date, sqFt, beds, details, term))

        return output
    
class Palatine(Bozzuto):
    def getPrice(self):
        return super().parseWebsite("https://www.palatineapts.com/availableunits", "Palatine")
    
class BeaconClarendon(Bozzuto):
    def getPrice(self):
        return super().parseWebsite("https://www.beaconarlington.com/availableunits", "Beacon Clarendon")
    
class RosslynHeights(Bozzuto):
    def getPrice(self):
        return super().parseWebsite("https://www.rosslynheights.com/availableunits", "Rosslyn Heights")