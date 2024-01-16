import json
from csv import DictReader

#Puts the contents of the json file into list 'precipitation'
with open('precipitation.json') as file:
    precipitation = json.load(file)

#Creates a list of dictionaries of the measurements at the Seattle station
precipitation_seattle = list()
for measurement in precipitation:
    if measurement['station'] == 'GHCND:US1WAKG0038':
        precipitation_seattle.append(measurement)

#Makes dictionary 'results' containing a key 'total_monthly_precipitation' with value a list with 12 elements (all 0)
results = dict()
results['total_monthly_precipitation'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
current_month = 0
#Loops through every month, counts total precipitation and adds it to the list
for month in results['total_monthly_precipitation']:
    current_month += 1
    current_month_index = current_month -1
    #Fixes month count so it matches with the date entries
    if current_month <= 9:
        current_month_str = '0' + str(current_month)
    #calculates total precipitation and adds it to right month
    else:
        current_month_str = str(current_month)
    for measurement in precipitation_seattle:
        if measurement['date'].startswith(f'2010-{current_month_str}'):
            results['total_monthly_precipitation'][current_month_index] += measurement['value']

#Dumps results into json file            
with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, indent=4)