# ICS-285663 - OOP Method
# Modules to install
# pip install pyexcel
# pip install pyexcel-text
# pip install matplotlib.pyplot

import csv
import sys
import os
import json
import pyexcel as pe
import matplotlib.pyplot as plt 


class Product:
    def __init__(self, objID, prodArr) -> None:
        self.objID = objID
        self.prodID = prodArr[0]
        self.marketPrices = [float(i) for i in prodArr[1:5]]
        self.marketPriceAvg = str(round(sum(self.marketPrices) / 4, 2))
        self.year = prodArr[5]

    def findBaseProd(self, baseProdTable):
        for row in baseProdTable:
            if row[0] == self.prodID:
                self.name = row[1]
                self.basePrice = row[3]
                self.changeRatio = str(round(float(self.marketPriceAvg) / float(self.basePrice), 2))

# Завантаження таблиць та створення об'єктів товарів

products = []
productsIDs = []

with open(sys.path[0] + "/table1.csv", "r", encoding="utf-8") as table1:
    prodTable = list(csv.reader(table1))
    del prodTable[0:2]
    for row in prodTable:
        products.append(Product(str(len(products)), row))
with open(sys.path[0] + "/table2.csv", "r", encoding="utf-8") as table2:
    baseProdTable = list(csv.reader(table2))
    del baseProdTable[0]
    for row in baseProdTable:
        productsIDs.append(row[0])
    for obj in products:
        obj.findBaseProd(baseProdTable)

# Заголовок таблиці

outputHeader = ("=" * 30) + " АНАЛІЗ ЗМІНИ РІВНЯ РИНКОВИХ ЦІН " + ("=" * 31)
outputTableHeader = ["Найменування товару", "Рік ", "Середня ринкова ціна, крб", "Роздрібна ціна, крб", "Рівень змін"]

# Функції виводу

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def printOutput(prodList=products, prodIDs=productsIDs):
    resultTable = []
    resultTable.append(outputTableHeader)
    for obj in prodList:
        if obj.prodID in prodIDs:
            resultTable.append(list([obj.name, obj.year, obj.marketPriceAvg, obj.basePrice, obj.changeRatio]))
        else:
            continue
    resultRender = pe.Sheet(resultTable)
    print(outputHeader)
    print(resultRender)
    input("Натисніть [Enter] щоб продовжити")
    clearConsole()
    return True

# Збереження на диску
def saveAsJSON():
    with open("result.json", "w", encoding="utf-8") as jf:
        jf.write(json.dumps([prod.__dict__ for prod in products]))
    print("File was saved as \"result.json\"")
    input("Натисніть [Enter] щоб продовжити")
    clearConsole()

def saveAsXlsx():
    resultTable = []
    resultTable.append(outputTableHeader)
    for obj in products:
        resultTable.append(list([obj.name, obj.year, obj.marketPriceAvg, obj.basePrice, obj.changeRatio]))
    pe.save_as(array = resultTable, dest_file_name = sys.path[0] + '/result.xlsx')
    print("File was saved as \"result.xlsx\"")
    input("Натисніть [Enter] щоб продовжити")
    clearConsole()

# Будування графіків
def marketPricesGrafic(prodID):
    x = [
        "2013.11.1", "2013.11.10", "2013.11.14", "2013.11.24",
        "2014.11.1", "2014.11.10", "2014.11.14", "2014.11.24",
        "2015.11.1", "2015.11.10", "2015.11.14", "2015.11.24"
    ]
    y = []
    for obj in products:
        if obj.prodID == prodID:
            basePrice = obj.basePrice
            name = obj.name
            for i in obj.marketPrices:
                y.append(float(i))
    plt.plot(x, y, marker="^", label="Ринкова ціна")
    plt.xlabel("Дати")
    plt.ylabel("Ціна, крб")
    plt.xticks(x, x, rotation=90)
    plt.plot(x, [float(basePrice) for i in range(len(x))], label="Роздрібна ціна")
    plt.subplots_adjust(bottom=0.2)
    plt.title("Ринкова ціна товару " + prodID + " : " + name)
    plt.legend()
    plt.show()

def marketPricesOfYearGrafic(prodID, year):
    pass
    x = [year + ".11.1", year + ".11.10", year + ".11.14", year + ".11.24"]
    y = []
    for obj in products:
        if obj.prodID == prodID:
            if obj.year == year:
                basePrice = obj.basePrice
                name = obj.name
                for i in obj.marketPrices:
                    y.append(float(i))
                break
    plt.plot(x, y, marker="^", label="Ринкова ціна")
    plt.xlabel("Дати")
    plt.ylabel("Ціна, крб")
    plt.xticks(x, x, rotation=90)
    plt.plot(x, [float(basePrice) for i in range(len(x))], label="Роздрібна ціна")
    plt.subplots_adjust(bottom=0.2)
    plt.title("Ринкова ціна товару " + prodID + " : " + name)
    plt.legend()
    plt.show()

# Вивід
clearConsole()
while True:
    print(
        " "*10 + "ЛАБОРАТОРНИЙ ПРАКТИКУМ" + " "*11, 
        " "*15 + "ЗАВДАННЯ № 1" + " "*16, 
        "з дисципліни «Уведення в комп’ютерні науки»", 
        sep="\n", end="\n\n"
        )
    print("Студент: Санжаров Данііл, ФІТ 1-7, 2 підгрупа. Семестр 1\n")
    print(
        "1. Вивести результуючу таблицю",
        "2. Зберегти у JSON",
        "3. Зберегти у xlsx",
        "4. Відобразити графік",
        "0. Вийти",
        sep="\n"
        )
    uInput = input("$ ")
    clearConsole()
    if uInput == "1":
        print(
            "Введіть коди товарів для відображення",
            "Розділяти пробілом",
            "Залишіть порожнім для відореження всіх",
            "Код : Товар",
            "50  : Картопля",
            "60  : Капуста",
            "70  : Цибуля",
            "80  : Мед",
            "90  : Часник",
            "100 : Яблука",
            sep="\n"
        )
        uInput = input("$ ").split(" ")
        clearConsole()
        if uInput != [""]:
            printOutput(products, uInput)
        else:
            printOutput(products)
    elif uInput == "2":
        saveAsJSON()
    elif uInput == "3":
        saveAsXlsx()
    elif uInput == "4":
        while True:
            print(
                "Оберіть графік",
                "1. Графік ринкової ціни",
                "2. Графік ринкової ціни за певний рік",
                "0. Назад",
                sep="\n"
            )
            uInput = input("$ ")
            clearConsole()
            if uInput == "1":
                while True:
                    print(
                        "Введіть код товару",
                        "Код : Товар",
                        "0   : Назад",
                        "50  : Картопля",
                        "60  : Капуста",
                        "70  : Цибуля",
                        "80  : Мед",
                        "90  : Часник",
                        "100 : Яблука",
                        sep="\n"
                    )
                    uInput = input("$ ")
                    clearConsole()
                    if uInput in productsIDs:
                        marketPricesGrafic(uInput)
                        break
                    elif uInput == "0":
                        break
                    else:
                        print("!!! Невідомий код !!!\n")
                        continue
            elif uInput == "2":
                while True:
                    print(
                        "Введіть код товару",
                        "Код : Товар",
                        "0   : Назад",
                        "50  : Картопля",
                        "60  : Капуста",
                        "70  : Цибуля",
                        "80  : Мед",
                        "90  : Часник",
                        "100 : Яблука",
                        sep="\n"
                    )
                    uInput1 = input("$ ")
                    clearConsole()
                    if uInput1 == "0":
                        break
                    print(
                        "Введіть рік",
                        "Доступні роки:",
                        "2013", "2014", "2015",
                        sep="\n"
                        )
                    uInput2 = input("$ ")
                    clearConsole()
                    if uInput1 in productsIDs and uInput2 in ["2013", "2014", "2015"]:
                        marketPricesOfYearGrafic(uInput1, uInput2)
                        break
                    elif uInput2 == "0":
                        break
                    else:
                        print("!!! Невідомий код !!!\n")
                        continue
            elif uInput == "0":
                break
    elif uInput == "0":
        clearConsole()
        break
    