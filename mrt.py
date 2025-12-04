# Stations data (dictionaries)
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

TicketType = ["SINGLEJOURNEY", "ADULT", "STUDENT", "SENIOR"]

class BTS_N_Extension_Fare:
    # ------------------------------------ Initial function ------------------------------------
    def __init__(self, StartStation, StopStation, Ticket):
        self.distance = abs(int(StartStation[1:]) - int(StopStation[1:]))   # คำนวณระยะทางให้เป็นจำนวนสถานี
        self._index = self.distance - 1                                     # ตัวนับระยะทาง
        self.loop = 0                                                       # ตัวนับอัตราการเพิ่มค่าโดยสาร
        self.ticket = Ticket                                                # ประเภทตั๋วโดยสาร
        self.StartStation = BTS_N_EXTENSION_STATIONS[StartStation]          # ต้นทาง
        self.StopStation = BTS_N_EXTENSION_STATIONS[StopStation]            # ปลายทาง
        self.net = 0                                                        # ค่าโดยสารสุทธิ

    # ------------------------------------ Base values------------------------------------
    StartPrice = {"SINGLEJOURNEY": 17, "ADULT": 17, "STUDENT": 12}          # ค่าโดยสารเริ่มต้นของบัตรแต่ละประเภท
    MaxPrice = {"SINGLEJOURNEY": 45, "ADULT": 45, "STUDENT": 32}            # ค่าโดยสารสูงสุดของบัตรแต่ละประเภท
    SINGLEJOURNEYIncreaseRate = [2, 3]                                      # อัตราการเพิ่มค่าโดยสารตั๋วเที่ยวเดียว
    ADULTIncreaseRate = [2, 3]                                              # อัตราการเพิ่มค่าโดยสารผู้ใหญ่
    STUDENTIncreaseRate = [2, 2, 2, 1]                                      # อัตราการเพิ่มค่าโดยสารนักศึกษา

    # ------------------------------------ Fare calculation process ------------------------------------
    def FareCalBase(self, TicketType, List, StartPrice = StartPrice):               # ฟังก์ชันกำหนดค่าการคำนวณ
        self.net += StartPrice[TicketType]                                              # ตั้งค่าค่าโดยสารเริ่มต้น
        increaseFormula = List                                                          # กำหนดอัตราการเพิ่มค่าโดยสาร
        MaxPrice = BTS_N_Extension_Fare.MaxPrice[TicketType]                            # กำหนดค่าโดยสารสูงสุด
        self.net = BTS_N_Extension_Fare.FareCalProcess(self, MaxPrice, increaseFormula) # เรียกใช้ฟังก์ชันคำนวณค่าโดยสาร ส่งค่าทั้งหมดเข้า function แล้ว recursive function

    def FareCalProcess(self, MaxPrice, increaseFormula):                            # ฟังก์ชันคำนวณค่าโดยสาร (recursive function)
        if self._index == 0: return self.net                                            # ถ้าตัวนับระยะทางเป็น 0 แล้ว หยุดการทำงาน
        self.net += increaseFormula[self.loop]                                          # เพิ่มค่าโดยสารตามอัตราที่กำหนด ตามตัวนับตำแหน่งของลิสต์อัตราค่าโดยสารในรอบนั้น ๆ
        if self.loop < len(increaseFormula) - 1: self.loop += 1                         # ถ้าตัวนับตำแหน่งของลิสต์อัตราค่าโดยสารยังไม่เกินตำแหน่งสุดท้าย ให้เพิ่มค่าตัวนับขึ้น 1
        else: self.loop = 0                                                             # แต่ถ้าเกินแล้ว ให้วนกลับไป 0 ใหม่
        if self.net >= MaxPrice: return MaxPrice                                        # ถ้าค่าโดยสารที่คำนวณมาเกินค่าที่กำหนดไว้ ให้ตั้งค่าเป็นค่าสูงสุดแล้ว หยุดการทำงาน
        self._index -= 1                                                                # ลดตัวนับระยะทางลง 1
        return self.FareCalProcess(MaxPrice, increaseFormula)                           # เรียกใช้ฟังก์ชันตัวเอง (recursive) อีกครั้ง (จะโดนเรียกซ้ำจนกว่าจะเจอเงื่อนไขหยุดการทำงาน)

    def calPrice(self):                                                             # ฟังก์ชันเลือกประเภทตั๋วโดยสาร
        match self.ticket:                                                              # เป็นบัตรประเภทไหน ให้ใช้ค่าโดยสารเริ่มต้น อัตราเพิ่ม และค่าโดยสารสูงสุดของบัตรนั้น ๆ
            case "ADULT":
                self.FareCalBase("ADULT", BTS_N_Extension_Fare.ADULTIncreaseRate)
            case "SINGLEJOURNEY":
                self.FareCalBase("SINGLEJOURNEY", BTS_N_Extension_Fare.SINGLEJOURNEYIncreaseRate)
            case "STUDENT":
                self.loop = 1
                self.FareCalBase("STUDENT", BTS_N_Extension_Fare.STUDENTIncreaseRate)
            case "SENIOR":
                self.FareCalBase("ADULT", BTS_N_Extension_Fare.ADULTIncreaseRate)       # คำนวณค่าโดยสารเหมือนบัตรผู้ใหญ่ แต่ลด 50% (หาร 2)
                self.net = (self.net + 1) // 2

    # ------------------------------------ Print trip details ------------------------------------
    def __repr__(self):
        return (f"\n"
                f"------------------------------------------------------------\n"
                f"Passenger card type: {self.ticket.capitalize()}\n"
                f"Origin station: {self.StartStation} \n"
                f"Destination station: {self.StopStation} \n"
                f"Distance traveling: {self.distance} station(s) \n"
                f"Fare (NET): {self.net} Baht\n"
                f"------------------------------------------------------------")

# ------------------------------------ Trip details function ------------------------------------
def TripDetails():
    Ticket = BTS_N_Extension_Fare(inputStartStation, inputStopStation, inputTicketType)
    Ticket.calPrice()
    print(Ticket)

### ------------------------------------ MAIN PROGRAM ------------------------------------ ###

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
