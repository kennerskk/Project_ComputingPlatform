BTS_N_EXTENSION_STATIONS_TH = {"N24": "คูคต",
                              "N23": "แยก คปอ.",
                              "N22": "พิพิธภัณฑ์กองทัพอากาศ",
                              "N21": "โรงพยาบาลภูมิพลอดุลยเดช",
                              "N20": "สะพานใหม่",
                              "N19": "สายหยุด",
                              "N18": "พหลโยธิน 59",
                              "N17": "วัดพระศรีมหาธาตุ",
                              "N16": "กรมทหารราบที่ 11",
                              "N15": "บางบัว",
                              "N14": "กรมป่าไม้",
                              "N13": "มหาวิทยาลัยเกษตรศาสตร์",
                              "N12": "เสนานิคม",
                              "N11": "รัชโยธิน",
                              "N10": "พหลโยธิน 24",
                              "N9": "ห้าแยกลาดพร้าว", }

BTS_N_EXTENSION_STATIONS_EN = {"N24": "Khu Khot",
                              "N23": "Yaek Kor Por Aor",
                              "N22": "Royal Thai Air Force Museum",
                              "N21": "Bhumibol Adulyadej Hospital",
                              "N20": "Saphan Mai",
                              "N19": "Sai Yud",
                              "N18": "Phahon Yothin 59",
                              "N17": "Wat Phra Sri Mahathat",
                              "N16": "11th Infantry Regiment",
                              "N15": "Bang Bua",
                              "N14": "Royal Forest Department",
                              "N13": "Kasetsart University",
                              "N12": "Sena Nikhom",
                              "N11": "Ratchayothin",
                              "N10": "Phahon Yothin 24",
                              "N9": "Ha Yaek Lat Phrao", }

TicketType = ["ADULT", "SINGLEJOURNEY", "STUDENT", "SENIOR"]

class BTS_N_Extension_Fare:
    def __init__(self, StartStation, StopStation, Ticket):
        self.distance = abs(int(StartStation[1:]) - int(StopStation[1:]))
        self._index = self.distance - 1
        self.loop = 0
        self.ticket = Ticket
        self.StartStation = BTS_N_EXTENSION_STATIONS[StartStation]
        self.StopStation = BTS_N_EXTENSION_STATIONS[StopStation]
        self.net = 0

    StartPrice = {"ADULT": 17, "SINGLEJOURNEY": 17, "STUDENT": 12}
    MaxPrice = {"ADULT": 45, "SINGLEJOURNEY": 45, "STUDENT": 32}
    ADULTIncreaseRate = [2, 3]
    SINGLEJOURNEYIncreaseRate = [2, 3]
    STUDENTIncreaseRate = [2, 2, 2, 1]

    def FareCalProcess(self, priceMax, increaseFormula):
        if self._index == 0: return self.net
        self.net += increaseFormula[self.loop]
        if self.loop < len(increaseFormula) - 1: self.loop += 1
        else: self.loop = 0
        if self.net >= priceMax: return priceMax
        self._index -= 1
        return self.FareCalProcess(priceMax, increaseFormula)

    def FareCalBase(self, TicketType, List, StartPrice = StartPrice):
        self.net += StartPrice[TicketType]
        increaseFormula = List
        MaxPrice = BTS_N_Extension_Fare.MaxPrice[TicketType]
        self.net = BTS_N_Extension_Fare.FareCalProcess(self, MaxPrice, increaseFormula)

    def calPrice(self):
        match self.ticket:
            case "ADULT":
                self.FareCalBase("ADULT", BTS_N_Extension_Fare.ADULTIncreaseRate)
            case "SINGLEJOURNEY":
                self.FareCalBase("SINGLEJOURNEY", BTS_N_Extension_Fare.SINGLEJOURNEYIncreaseRate)
            case "STUDENT":
                self.loop = 1
                self.FareCalBase("STUDENT", BTS_N_Extension_Fare.STUDENTIncreaseRate)
            case "SENIOR":
                self.FareCalBase("ADULT", BTS_N_Extension_Fare.ADULTIncreaseRate)
                self.net = (self.net + 1) // 2

    def __repr__(self):
        return (f"\n"
                f"------------------------------------------------------------\n"
                f"Passenger card type: {self.ticket.capitalize()}\n"
                f"Origin station: {self.StartStation} \n"
                f"Destination station: {self.StopStation} \n"
                f"Distance traveling: {self.distance} station(s) \n"
                f"Fare (NET): {self.net} Baht\n"
                f"------------------------------------------------------------")

def TripDetails():
    Ticket = BTS_N_Extension_Fare(inputStartStation, inputStopStation, inputTicketType)
    Ticket.calPrice()
    print(Ticket)

# ------------------------------------ MAIN PROGRAM ------------------------------------

print("------------------------------------------------------------\n"
      "BTS SKYTRAIN: Northern Extension Fare Calculation System\n"
      "------------------------------------------------------------")

# 1. Language selection
while True:
    try:
        lang_input = input("  > Select a language (EN, TH): ").upper()
        if lang_input == "TH": BTS_N_EXTENSION_STATIONS = BTS_N_EXTENSION_STATIONS_TH
        elif lang_input == "EN": BTS_N_EXTENSION_STATIONS = BTS_N_EXTENSION_STATIONS_EN
        else: raise ValueError
        break
    except ValueError:
        print("Invalid input. Try again.")
        continue

# 2. Stations and card type selection
for i in BTS_N_EXTENSION_STATIONS:
    print(f"[{i}] {BTS_N_EXTENSION_STATIONS[i]}")
while True:
    try:
        inputStartStation = input("  > Enter your origin station code: ").upper()
        BTS_N_EXTENSION_STATIONS[inputStartStation]
        break
    except KeyError:
        print("Invalid station code. Please try again.")
while True:
    try:
        inputStopStation = input("  > Enter your destination station code: ").upper()
        BTS_N_EXTENSION_STATIONS[inputStopStation]
        break
    except KeyError:
        print("Invalid station code. Please try again.")
while True:
    try:
        inputTicketType = input("  > Enter your ticket type (Adult, SingleJourney, Student, Senior): ").upper()
        if inputTicketType not in TicketType: raise ValueError
        break
    except ValueError:
        print("Invalid ticket type. Please try again.")

# 3. Print trip details
TripDetails()
