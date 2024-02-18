from datetime import datetime
from bs4 import BeautifulSoup
from Apartment import Apartment
from Option import Option
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List

class Greystar(Apartment):
    def parseWebsite(self, url, building) -> List[Option]:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        apts = soup.find_all("li", {"class": "floorplan-listing__item"})

        output = []

        for apt in apts:
            price = apt.find("p", {"class": "floorplan-listing__price"}).text.replace("Starting at ", "")
            if ("Contact Us" in price):
                continue

            sqFt = int(apt.find("p", {"class": "floorplan-listing__info"}).text.split(" | ")[2].split()[0].replace(",", ""))
            beds = apt.find("p", {"class": "floorplan-listing__info"}).text.split(" | ")[0]
            term = "15 mo. lease"
            date = datetime.today()
            id = apt.find("p", {"class": "floorplan-listing__title"}).text

            output.append(Option(building, id, price, date, sqFt, beds, "", term))

        return output
    
class Commodore(Greystar):
    def getPrice(self):
        return super().parseWebsite("https://livethecommodore.com/floorplans/", "Commodore")