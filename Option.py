import datetime

class Option:
    def __init__(self, buildingName, id, price, availableDate, sqFt, beds, details, term):
        self.building = buildingName.strip()
        self.price = int(price.strip().replace("$", "").replace(",", ""))
        self.id = id.strip()
        self.date = availableDate
        self.sqFt = sqFt
        self.beds = beds.replace("Bed", "").strip()
        self.details = details.strip().strip(", ")
        self.term = term.strip()

        if self.date == "TBD":
            self.date = None

    def __str__(self):
        return f"{self.building} {self.id}: {self.price} ({self.term}), _{self.sqFt}_ sq ft, _{self.beds}_ bed, {self.details}, {self.date}"