from datetime import datetime
from typing import Any
from bs4 import BeautifulSoup, ResultSet
from Apartment import Apartment
from Option import Option
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class Avalon(Apartment):
    def parseWebsite(self, url) -> ResultSet[Any]:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        try:
            python_button = driver.find_element(By.CSS_SELECTOR, '.anticon-close')
            python_button.click()
        except:
            pass
            
        try:
            # Selenium doesn't think we can click it, so we do so anyways
            python_button = driver.find_element(By.ID, 'load-all-units')
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(python_button, 0, 0)
            action.click()
            action.perform()
        except:
            pass

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup.find_all("div", {"class": "unit-item-details"})


class AvalonCourthousePlace(Avalon):
    def getPrice(self):
        apts = super().parseWebsite("https://www.avaloncommunities.com/virginia/arlington-apartments/avalon-courthouse-place/")

        output = []

        for apt in apts:
            price = apt.find("span", {"class": "unit-price"}).text
            id = apt.find("div", {"class": "ant-card-meta-title"}).text.replace("Avalon Courthouse Place", "").replace("Apt. ", "")
            date = datetime.strptime(apt.find("div", {"class": "available-date"}).text + " 2024", '%b %d %Y')
            package = apt.find("span", {"class": "finish-package-label"}).text
            term = apt.find("span", {"class": "term-length"}).text.replace("/ ", "")
            beds = apt.find("div", {"class": "description"}).text.split(" • ")[0].split()[0]
            sqFt = int(apt.find("div", {"class": "description"}).text.split(" • ")[2].split()[0])
            withDen = "with den" if (sqFt > 800 and sqFt < 1000) else ""


            if "Furnished" in package:
                continue

            output.append(Option("Avalon Courthouse Place", id, price, date, sqFt, beds, f"{withDen}, {package}", term))

        return output

class AvalonClarendon(Avalon):
    def getPrice(self):
        apts = super().parseWebsite("https://www.avaloncommunities.com/virginia/arlington-apartments/avalon-clarendon/")

        output = []

        for apt in apts:
            price = apt.find("span", {"class": "unit-price"}).text
            id = apt.find("div", {"class": "ant-card-meta-title"}).text.replace("Avalon Clarendon", "")
            date = datetime.strptime(apt.find("div", {"class": "available-date"}).text + " 2024", '%b %d %Y')
            term = apt.find("span", {"class": "term-length"}).text.replace("/ ", "")
            beds = apt.find("div", {"class": "description"}).text.split(" • ")[0].split()[0]
            sqFt = int(apt.find("div", {"class": "description"}).text.split(" • ")[2].split()[0])
            withDen = "with den" if (sqFt > 800 and sqFt < 1000) else ""


            if "Furnished" in beds:
                continue

            output.append(Option("Avalon Clarendon", id, price, date, sqFt, beds, withDen, term))

        return output
    
class AvalonBallstonSquare(Avalon):
    def getPrice(self):
        apts = super().parseWebsite("https://www.avaloncommunities.com/virginia/arlington-apartments/ava-ballston-square/")

        output = []

        for apt in apts:
            price = apt.find("span", {"class": "unit-price"}).text
            id = apt.find("div", {"class": "ant-card-meta-title"}).text.replace("AVA Ballston Square", "")
            date = datetime.strptime(apt.find("div", {"class": "available-date"}).text + " 2024", '%b %d %Y')
            term = apt.find("span", {"class": "term-length"}).text.replace("/ ", "")
            beds = apt.find("div", {"class": "description"}).text.split(" • ")[0].split()[0]
            sqFt = int(apt.find("div", {"class": "description"}).text.split(" • ")[2].split()[0])
            package = apt.find("span", {"class": "finish-package-label"}).text
            output.append(Option("AVA Ballston Square", id, price, date, sqFt, beds, package, term))

        return output