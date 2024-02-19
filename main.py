from Avalon import *
from Ditmar import *
from Bozzuto import *
from Equity import *
from Greystar import *
from Paradigm import *
from Kettler import *
import mysql.connector

apartments = [
    AvalonCourthousePlace(), 
    AvalonClarendon(), 
    AvalonBallstonSquare(),
    Palatine(), 
    BeaconClarendon(), 
    RosslynHeights(),
    Nineteen19(),
    CourtlandTowers(), 
    Amelia(), 
    RichmondSquare(), 
    QuincyPlaza(), 
    RandolphTowers(), 
    CourtlandPark(), 
    VirginiaSquarePlaza(), 
    VirginiaSquareTowers(), 
    TheEarl(),
    TheClarendon(), 
    Wilson2201(), 
    CourthousePlaza(), 
    LibertyTower(), 
    Oak1800(), 
    ThePrime(), 
    ReserveAtClarendon(),
    Commodore(), 
    GarfieldPark(),
    MeridianCourthouse(), 
    MeridianBallston(), 
]

mydb = mysql.connector.connect(
  host="localhost",
  user="dev",
  password="1234",
  database="apt_hunting"
)

mycursor = mydb.cursor()

for apt in apartments:
    print(apt)
    i = 0
    apts = []
    while i < 3:
       try:
            apts = apt.getPrice()
       except:
           pass
       if len(apts) == 0:
           i = i + 1
           print(f"No apts found, retrying ({i})")
       else:
           break

    for unit in apts:
        print(unit)
        sql = "INSERT INTO info (building, aptId, price, available, sqFt, beds, details, term) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (unit.building, unit.id, unit.price, unit.date, unit.sqFt, unit.beds, unit.details, unit.term)
        mycursor.execute(sql, val)
    mydb.commit()
