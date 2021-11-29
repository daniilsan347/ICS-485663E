# ICS-485663E - OOP Method
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
from time import sleep

import tkinter as tk
import tkinter.ttk as ttk

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

def tableSelect():
    tabSelWin = tk.Toplevel(rootWin)
    tabSelWin.title("Таблиця №3 - Настройки")
    tabSelWin.resizable(False, False)
    lbl2 = tk.Label(tabSelWin, text = "Оберіть товар").pack()
    prodIDsCheckBtn = [
        tk.StringVar(tabSelWin, "50"), 
        tk.StringVar(tabSelWin, "60"),
        tk.StringVar(tabSelWin, "70"),
        tk.StringVar(tabSelWin, "80"),
        tk.StringVar(tabSelWin, "90"),
        tk.StringVar(tabSelWin, "100")
        ]
    tk.Checkbutton(tabSelWin, text="Картопля", variable=prodIDsCheckBtn[0], onvalue="50" , offvalue="None").pack(side=tk.LEFT, padx = 10)
    tk.Checkbutton(tabSelWin, text="Капуста" , variable=prodIDsCheckBtn[1], onvalue="60" , offvalue="None").pack(side=tk.LEFT, padx = 10)
    tk.Checkbutton(tabSelWin, text="Цибуля"  , variable=prodIDsCheckBtn[2], onvalue="70" , offvalue="None").pack(side=tk.LEFT, padx = 10)
    tk.Checkbutton(tabSelWin, text="Мед"     , variable=prodIDsCheckBtn[3], onvalue="80" , offvalue="None").pack(side=tk.LEFT, padx = 10)
    tk.Checkbutton(tabSelWin, text="Часник"  , variable=prodIDsCheckBtn[4], onvalue="90" , offvalue="None").pack(side=tk.LEFT, padx = 10)
    tk.Checkbutton(tabSelWin, text="Яблука"  , variable=prodIDsCheckBtn[5], onvalue="100", offvalue="None").pack(side=tk.LEFT, padx = 10)
    tk.Button(tabSelWin, text = "Вивести таблицю", command = lambda:showOutput(prodIDs = [i.get() for i in prodIDsCheckBtn])).pack()
    
def showOutput(prodList=products, prodIDs=productsIDs):
    print(prodIDs)
    resultTable = []
    for obj in prodList:
        if obj.prodID in prodIDs:
            resultTable.append(list([obj.name, obj.year, obj.marketPriceAvg, obj.basePrice, obj.changeRatio]))
        else:
            continue

    columns = ("#1", "#2", "#3", "#4", "#5")
    tabWin = tk.Toplevel(rootWin)
    tabWin.title("Таблиця №3")
    tree = ttk.Treeview(tabWin, show="headings", columns=columns)
    tree.heading("#1", text = "Найменування товару")
    tree.heading("#2", text = "Рік")
    tree.heading("#3", text = "Середня ринкова ціна, крб")
    tree.heading("#4", text = "Роздрібна ціна, крб")
    tree.heading("#5", text = "Рівень змін")
    ysb = ttk.Scrollbar(tabWin, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=ysb.set)

    for row in resultTable:
        tree.insert("", tk.END, values=row)
    tree.grid(row=0, column=0)
    ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
    tabWin.rowconfigure(0, weight=1)
    tabWin.columnconfigure(0, weight=1)

def graficSel():
    grafSelWin = tk.Toplevel(rootWin)
    grafSelWin.resizable(False, False)
    grafSelWin.geometry("190x480")

    global radioType
    radioType = tk.StringVar(grafSelWin, "Price")
    tk.Label(grafSelWin, text = "Оберіть тип графіка").pack(anchor = tk.W, pady = 10, padx = 10)
    tk.Radiobutton(grafSelWin, text = "Ціна за весь період", variable = radioType, value = "Price").pack(anchor = tk.W)
    tk.Radiobutton(grafSelWin, text = "Ціна за певний рік" , variable = radioType, value = "PriceByYear" ).pack(anchor = tk.W)
    tk.Radiobutton(grafSelWin, text = "Зміни за певний рік" , variable = radioType, value = "Ratio" ).pack(anchor = tk.W)
    tk.Radiobutton(grafSelWin, text = "Зміни за певний рік" , variable = radioType, value = "RatioByYear" ).pack(anchor = tk.W)

    global radioProd
    radioProd = tk.StringVar(grafSelWin, "50")
    tk.Label(grafSelWin, text = "Оберіть товар").pack(anchor = tk.W, pady = 10, padx = 10)
    tk.Radiobutton(grafSelWin, text = "Картопля", variable = radioProd, value = "50" ).pack(anchor = tk.W)
    tk.Radiobutton(grafSelWin, text = "Капуста" , variable = radioProd, value = "60" ).pack(anchor = tk.W)
    tk.Radiobutton(grafSelWin, text = "Цибуля"  , variable = radioProd, value = "70" ).pack(anchor = tk.W)
    tk.Radiobutton(grafSelWin, text = "Мед"     , variable = radioProd, value = "80" ).pack(anchor = tk.W)
    tk.Radiobutton(grafSelWin, text = "Часник"  , variable = radioProd, value = "90" ).pack(anchor = tk.W)
    tk.Radiobutton(grafSelWin, text = "Яблука"  , variable = radioProd, value = "100").pack(anchor = tk.W)

    global radioYear
    radioYear = tk.StringVar(grafSelWin, "2013")
    tk.Label(grafSelWin, text = "Рік").pack(anchor = tk.W, pady = 10, padx = 10)
    tk.Radiobutton(grafSelWin, text = "2013", variable = radioYear, value = "2013").pack(anchor = tk.W)
    tk.Radiobutton(grafSelWin, text = "2014", variable = radioYear, value = "2014").pack(anchor = tk.W)
    tk.Radiobutton(grafSelWin, text = "2015", variable = radioYear, value = "2015").pack(anchor = tk.W)

    tk.Button(grafSelWin, text = "Побудувати графік", command = graficSelProc, height = 2, width = 26).pack()

def graficSelProc():
    if radioType.get() == "Price":
        marketPricesGrafic(radioProd.get())
    elif radioType.get() == "PriceByYear":
        marketPricesOfYearGrafic(radioProd.get(), radioYear.get())
    elif radioType.get() == "Ratio":
        ratioGrafic(radioProd.get())
    elif radioType.get() == "RatioByYear":
        ratioOfYearGrafic(radioProd.get(), radioYear.get())

# def printOutput(prodList=products, prodIDs=productsIDs):
#     resultTable = []
#     resultTable.append(outputTableHeader)
#     for obj in prodList:
#         if obj.prodID in prodIDs:
#             resultTable.append(list([obj.name, obj.year, obj.marketPriceAvg, obj.basePrice, obj.changeRatio]))
#         else:
#             continue
#     resultRender = pe.Sheet(resultTable)
#     print(outputHeader)
#     print(resultRender)
#     input("Натисніть [Enter] щоб продовжити")
#     clearConsole()
#     return True

# Збереження на диску
def saveAsJSON():
    with open("result.json", "w", encoding="utf-8") as jf:
        jf.write(json.dumps([prod.__dict__ for prod in products]))
    print("File was saved as \"result.json\"")
    lbl1['text'] = "Збереженно до \"./result.json\""

def saveAsXlsx():
    resultTable = []
    resultTable.append(outputTableHeader)
    for obj in products:
        resultTable.append(list([obj.name, obj.year, obj.marketPriceAvg, obj.basePrice, obj.changeRatio]))
    pe.save_as(array = resultTable, dest_file_name = sys.path[0] + '/result.xlsx')
    print("File was saved as \"result.xlsx\"")
    lbl1['text'] = "Збереженно до \"./result.xlsx\""
    lbl1.pack()

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

def ratioGrafic(prodID):
    x = [
        "2013.11.1", "2013.11.10", "2013.11.14", "2013.11.24",
        "2014.11.1", "2014.11.10", "2014.11.14", "2014.11.24",
        "2015.11.1", "2015.11.10", "2015.11.14", "2015.11.24"
    ]
    y = []
    for obj in products:
        if obj.prodID == prodID:
            name = obj.name
            for i in obj.marketPrices:
                y.append(float(i)/float(obj.basePrice))
    plt.plot(x, y, marker="^", label="Зміни")
    plt.xlabel("Дати")
    plt.ylabel("Рівень змін")
    plt.xticks(x, x, rotation=90)
    plt.subplots_adjust(bottom=0.2)
    plt.title("Рівень змін відносно роздрібної ціни товару " + prodID + " : " + name)
    plt.legend()
    plt.show()

def marketPricesOfYearGrafic(prodID, year):
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

def ratioOfYearGrafic(prodID, year):
    x = [year + ".11.1", year + ".11.10", year + ".11.14", year + ".11.24"]
    y = []
    for obj in products:
        if obj.prodID == prodID:
            if obj.year == year:
                name = obj.name
                for i in obj.marketPrices:
                    y.append(float(i)/float(obj.basePrice))
                break
    plt.plot(x, y, marker="^", label="Зміни")
    plt.xlabel("Дати")
    plt.ylabel("Рівень змін")
    plt.xticks(x, x, rotation=90)
    plt.subplots_adjust(bottom=0.2)
    plt.title("Рівень змін відносно роздрібної ціни товару " + prodID + " : " + name)
    plt.show()

# Вивід

rootWin = tk.Tk()
rootWin.title("Головне меню")
rootWin.geometry("190x185")
rootWin.resizable(False, False)

btn1 = tk.Button(rootWin, text = "Вивести таблицю", height = 2, width = 26, command = tableSelect)
btn2 = tk.Button(rootWin, text = "Зберегти у JSON", height = 2, width = 26, command = saveAsJSON)
btn3 = tk.Button(rootWin, text = "Зберегти у xlsx", height = 2, width = 26, command = saveAsXlsx)
btn4 = tk.Button(rootWin, text = "Вивести графік",  height = 2, width = 26, command = graficSel)
lbl1 = tk.Label (rootWin, text = "")

btn1.pack()
btn2.pack()
btn3.pack()
btn4.pack()
lbl1.pack()

rootWin.mainloop()

# clearConsole()
# while True:
#     print(
#         " "*10 + "ЛАБОРАТОРНИЙ ПРАКТИКУМ" + " "*11, 
#         " "*15 + "ЗАВДАННЯ № 1" + " "*16, 
#         "з дисципліни «Уведення в комп’ютерні науки»", 
#         sep="\n", end="\n\n"
#         )
#     print("Студент: Санжаров Данііл, ФІТ 1-7, 2 підгрупа. Семестр 1\n")
#     print(
#         "1. Вивести результуючу таблицю",
#         "2. Зберегти у JSON",
#         "3. Зберегти у xlsx",
#         "4. Відобразити графік",
#         "0. Вийти",
#         sep="\n"
#         )
#     uInput = input("$ ")
#     clearConsole()
#     if uInput == "1":
#         print(
#             "Введіть коди товарів для відображення",
#             "Розділяти пробілом",
#             "Залишіть порожнім для відореження всіх",
#             "Код : Товар",
#             "50  : Картопля",
#             "60  : Капуста",
#             "70  : Цибуля",
#             "80  : Мед",
#             "90  : Часник",
#             "100 : Яблука",
#             sep="\n"
#         )
#         uInput = input("$ ").split(" ")
#         clearConsole()
#         if uInput != [""]:
#             printOutput(products, uInput)
#         else:
#             printOutput(products)
#     elif uInput == "2":
#         saveAsJSON()
#     elif uInput == "3":
#         saveAsXlsx()
#     elif uInput == "4":
#         while True:
#             print(
#                 "Оберіть графік",
#                 "1. Графік ринкової ціни",
#                 "2. Графік ринкової ціни за певний рік",
#                 "0. Назад",
#                 sep="\n"
#             )
#             uInput = input("$ ")
#             clearConsole()
#             if uInput == "1":
#                 while True:
#                     print(
#                         "Введіть код товару",
#                         "Код : Товар",
#                         "0   : Назад",
#                         "50  : Картопля",
#                         "60  : Капуста",
#                         "70  : Цибуля",
#                         "80  : Мед",
#                         "90  : Часник",
#                         "100 : Яблука",
#                         sep="\n"
#                     )
#                     uInput = input("$ ")
#                     clearConsole()
#                     if uInput in productsIDs:
#                         marketPricesGrafic(uInput)
#                         break
#                     elif uInput == "0":
#                         break
#                     else:
#                         print("!!! Невідомий код !!!\n")
#                         continue
#             elif uInput == "2":
#                 while True:
#                     print(
#                         "Введіть код товару",
#                         "Код : Товар",
#                         "0   : Назад",
#                         "50  : Картопля",
#                         "60  : Капуста",
#                         "70  : Цибуля",
#                         "80  : Мед",
#                         "90  : Часник",
#                         "100 : Яблука",
#                         sep="\n"
#                     )
#                     uInput1 = input("$ ")
#                     clearConsole()
#                     if uInput1 == "0":
#                         break
#                     print(
#                         "Введіть рік",
#                         "Доступні роки:",
#                         "2013", "2014", "2015",
#                         sep="\n"
#                         )
#                     uInput2 = input("$ ")
#                     clearConsole()
#                     if uInput1 in productsIDs and uInput2 in ["2013", "2014", "2015"]:
#                         marketPricesOfYearGrafic(uInput1, uInput2)
#                         break
#                     elif uInput2 == "0":
#                         break
#                     else:
#                         print("!!! Невідомий код !!!\n")
#                         continue
#             elif uInput == "0":
#                 break
#     elif uInput == "0":
#         clearConsole()
#         break
    