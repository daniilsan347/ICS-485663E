# ICS-285663 - OOP Method

import csv
import sys
import platform


class Product:
    objID = None
    prodID = None
    year = None
    name = None
    marketPrices = []
    marketPriceAvg = None
    basePrice = None
    changeRatio = None

    def __init__(self, objID, prodArr) -> None:
        self.objID = objID
        self.prodID = prodArr[0]
        # self.marketPrices = prodArr[1:4]
        self.marketPrices = [float(i) for i in prodArr[1:4]]
        self.marketPriceAvg = str(round(sum(self.marketPrices) / 4, 2))
        self.year = prodArr[5]

    def findBaseProd(self, baseProdTable):
        for row in baseProdTable:
            if row[0] == self.prodID:
                self.name = row[1]
                self.basePrice = row[3]
                self.changeRatio = str(
                    round(float(self.marketPriceAvg) / float(self.basePrice), 2)
                )


# Гемор с кодировками
fileNames = None
currentOS = platform.system()
if currentOS == "Windows":
    fileNames = ("/table1.win1521.csv", "/table2.win1521.csv")
elif currentOS == "Linux" or currentOS == "Darwin":  # Darwin == OSX
    fileNames = ("/table1.utf8.csv", "/table2.utf8.csv")


products = []

with open(sys.path[0] + fileNames[0], "r") as table1:
    prodTable = list(csv.reader(table1))
    del prodTable[0:2]
    for row in prodTable:
        products.append(Product(str(len(products)), row))
with open(sys.path[0] + fileNames[1], "r") as table2:
    baseProdTable = list(csv.reader(table2))
    del baseProdTable[0]
    for obj in products:
        obj.findBaseProd(baseProdTable)
