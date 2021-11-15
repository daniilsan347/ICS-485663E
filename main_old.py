#pip install pyexcel
#pip install pyexcel-ods
#pip install pyexcel-xlsx
#pip install pyexcel-text

import pyexcel as pe

pricesTable = pe.get_array(file_name = "./table1.ods")
goodsTable = pe.get_array(file_name = "./table2.ods")

pe.free_resources()

prices = []

for row in pricesTable:
  if type(row[0]) == str:
    continue
  prices.append(dict({'id':row[0], 'avg':round(sum(row[1:4])/4, 2), 'year':row[5]})) 

goods = {}

for row in goodsTable:
  if type(row[0]) == str:
    continue
  goods[row[0]] = {}
  goods[row[0]]['name'] = row[1]
  goods[row[0]]['price'] = row[3]

resultTable = [['Найменування товару', 'Рік', 'Середня ціна, крб', 'Розднібна ціна, крб', 'Рівень змін']]

index = 1
for row in prices:
  resultTable.append([])
  resultTable[index].append(goods[row['id']]['name'])
  resultTable[index].append(row['year'])
  resultTable[index].append(row['avg'])
  resultTable[index].append(goods[row['id']]['price'])
  resultTable[index].append(round(row['avg']/goods[row['id']]['price'], 2))
  index += 1

resultRender = pe.Sheet(resultTable)

print(resultRender.orgtbl)
print('\n')

while True:
  user_input = input('Зберігати у файл? [Y/N] ')
  if user_input.lower() == 'n':
    break
  elif user_input.lower() == 'y':
    fileName = input('Назва файлу: ')
    print('Оберіть формат:')
    print('OpenDocument Sheet [ODS]')
    print('MS Excel 2007-365 [XLSX]')
    print('Скасувати [N]')
    user_input = input('> ')

    if user_input.lower() == 'ods':
      pe.save_as(array = resultTable, dest_file_name = fileName + '.ods')
      break
    elif user_input.lower() == 'xlsx':
      pe.save_as(array = resultTable, dest_file_name = fileName + '.xlsx')
      break
    elif user_input.lower() == 'n':
      break