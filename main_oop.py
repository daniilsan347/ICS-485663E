# ICS-285663 - OOP Method

import csv
import sys


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
        self.marketPrices = prodArr[1:4]
        self.marketPriceAvg = sum(self.marketPrices) / 4
        self.year = prodArr[5]

    def findBaseProd(baseProdTable):
        for row in baseProdTable:
            if row[0] == self.prodID:
                self.name = row[1]
                self.basePrice = row[3]
                self.changeRatio = round(self.marketPriceAvg / self.basePrice, 2)


products = []
with open(sys.path[0] + "/table1.csv", "r") as table1:
    prodTable = csv.reader(table1)
    # del prodTable[0:1]
    # for row in range(2, len(prodTable)):
    #     products.append(Product(len(products), row))
    for row in prodTable:
        print(row[0])
with open(sys.path[0] + "/table2.csv", "r") as table2:
    baseProdTable = csv.reader(table2)
    del baseProdTable[0]
    for obj in products:
        obj.findBaseProd(baseProdTable)

print(products)
