import json
from datetime import date, datetime, timedelta

file_path = "data.json"

current_date = str(date.today())
print(current_date)

try:
    with open(file_path, 'r') as file:
        data = json.load(file)
        print('Дата в файле ', data['date'])
        print(data)
except (FileNotFoundError, json.JSONDecodeError):
    data = {'date': None}

if data.get('date') != current_date:
    print('Даті не совпадают. Обновляем дату')
    data['date'] = current_date

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print("Файл обновлен")
else:
    print('Дата совпадает')
