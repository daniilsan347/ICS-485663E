import pyexcel as pe

pricesTable = pe.get_array(file_name="./table1.ods")
goodsTable = pe.get_array(file_name="./table2.ods")

pe.free_resources()

prices = []
goods = {}

for row in pricesTable:
  if type(row[0]) == str:
    continue
  prices.append(dict({'id':row[0], 'avg':round(sum(row[1:4])/4, 2), 'year':row[5]})) 

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

  user_input = input('Зберегти у файл *.xlsx ? [Y/N] ')

  if user_input.lower() == 'y':
    user_input = input('Назва файлу: ')
    pe.save_as(array = resultTable, dest_file_name = user_input + '.xlsx')
    break
  elif user_input.lower() == 'n':
    break