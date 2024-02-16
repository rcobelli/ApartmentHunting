from datetime import datetime
import time
from bs4 import BeautifulSoup
from Apartment import Apartment
from Option import Option
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List

class Ditmar(Apartment):
    def parseWebsite(self, url, building) -> List[Option]:
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        apts = soup.find_all("li", {"class": "fp-group-item"})

        output = []

        for apt in apts:
            date = apt.find("a", {"class": "primary-action"}).text.replace("Available ", "")
            if date == "Get Notified":
                continue
            elif date == "Only One Left!" or "Available" in date:
                date = datetime.today()
            else:
                date = datetime.strptime(date, '%b %d, %Y')

            sqFt = int(apt.find("div", {"class": "sq-feet"}).text.replace("Sq. Ft", "").replace("+", "").replace(",", ""))
            beds = apt.find("div", {"class": "bed-bath"}).find("span", {"class": "fp-col-text"}).text.split()[0]
            term = "12 mo. lease"
            withDen = "with den" if ("DEN" in apt.find("a", {"class": "fp-name-link"}).text) else ""
            price = apt.find("div", {"class": "rent"}).text.replace("Rent", "").replace("From", "").replace("/month", "")
            id = apt.find("a", {"class": "fp-name-link"}).text.replace("(30-DAY STAY AVAILABLE)", "").replace("(30-day stay available)", "").replace("(30-Day Stay Available)", "")

            if "FURNISHED" in id:
                continue

            output.append(Option(building, id, price, date, sqFt, beds, withDen, term))

        return output
    
class CourtlandTowers(Ditmar):
    def getPrice(self):
        return super().parseWebsite("https://www.rentctwr.com/arlington-vaapartments/courtland-towers/conventional/", "Courtland Towers")

class Amelia(Ditmar):
    def getPrice(self):
        return super().parseWebsite("https://www.renttheamelia.com/arlington-vaapartments/the-amelia/conventional/", "Amelia")

class RichmondSquare(Ditmar):
    def getPrice(self):
        return super().parseWebsite("https://www.rentrsq.com/arlington-vaapartments/richmond-square/conventional/", "Richmond Square")

class QuincyPlaza(Ditmar):
    def getPrice(self):
        return super().parseWebsite("https://www.rentqp.com/arlington-vaapartments/quincy-plaza/conventional/", "Quincy Plaza")

class RandolphTowers(Ditmar):
    def getPrice(self):
        return super().parseWebsite("https://www.rentrt.com/arlington-vaapartments/randolph-towers/conventional/", "Randolph Towers")

class CourtlandPark(Ditmar):
    def getPrice(self):
        return super().parseWebsite("https://www.rentctpk.com/arlington-vaapartments/courtland-park/conventional/", "Courtland Park")

class VirginiaSquarePlaza(Ditmar):
    def getPrice(self):
        return super().parseWebsite("https://www.rentvsp.com/arlington-va-apartments/virginia-square-plaza/conventional/", "Virginia Square Plaza")

class VirginiaSquareTowers(Ditmar):
    def getPrice(self):
        return super().parseWebsite("https://www.rentvst.com/arlington-valuxuryapartments/virginia-square-towers/conventional/", "Virginia Square Towers")