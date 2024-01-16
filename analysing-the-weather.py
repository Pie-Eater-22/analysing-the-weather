import json
from csv import DictReader

#Puts contents of json file into list 'precipitation'
with open('precipitation.json') as file:
    precipitation = json.load(file)

#Makes list of dictionaries describing the stations
with open('stations.csv') as file:
    items = list(DictReader(file))

#Makes dictionary 'results'
results = dict()

#Calculates yearly precipitation
total_yearly_precipitation = 0
measurement_index = -1
for measurement in precipitation:
    measurement_index += 1
    total_yearly_precipitation += precipitation[measurement_index]['value']

#Adds all results per location to 'results'
location_index = -1
for location in items:
    location_index += 1
    #Makes dictionary containing local information
    results[f'{items[location_index]['Location']}'] = dict()

    #Adds station and state to dictionary
    results[f'{items[location_index]['Location']}']['station'] = items[location_index]['Station']
    results[f'{items[location_index]['Location']}']['state'] = items[location_index]['State']

    #Makes list of dictionaries of the measurements at the local station
    precipitation_local = list()
    for measurement in precipitation:
        if measurement['station'] == f'{items[location_index]['Station']}':
            precipitation_local.append(measurement)
    #Makes dictionary 'results' containing list 'total_monthly_precipitation' with 12 elements (all 0)
    results[f'{items[location_index]['Location']}']['total_monthly_precipitation'] = [0,0,0,0,0,0,0,0,0,0,0,0]
    current_month = 0
    #Loops for every month, counts total precipitation and adds it to the list
    for month in results[f'{items[location_index]['Location']}']['total_monthly_precipitation']:
        current_month += 1
        current_month_index = current_month -1
        #Fixes month count so it matches with the date entries
        if current_month <= 9:
            current_month_str = '0' + str(current_month)
        else:
            current_month_str = str(current_month)
        #calculates total precipitation and adds it to right month
        for measurement in precipitation_local:
            if measurement['date'].startswith(f'2010-{current_month_str}'):
                results[f'{items[location_index]['Location']}']['total_monthly_precipitation'][current_month_index] += measurement['value']

    #Calculates total yearly precipitation and adds it to the dictionary
    total_yearly_precipitation_local = 0
    for measurement in precipitation_local:
        total_yearly_precipitation_local += measurement['value']
    results[f'{items[location_index]['Location']}']['total_yearly_precipitation'] = total_yearly_precipitation_local

    #Adds list 'relative_monthly_precipitation' with 12 elements (all 0) to dictionary 'results'
    results[f'{items[location_index]['Location']}']['relative_monthly_precipitation'] = [0,0,0,0,0,0,0,0,0,0,0,0]
    current_month = -1
    #Loops for every month, calculates relative precipitation and adds it to the list
    for month_relative in results[f'{items[location_index]['Location']}']['relative_monthly_precipitation']:
        current_month += 1
        results[f'{items[location_index]['Location']}']['relative_monthly_precipitation'][current_month] = int(results[f'{items[location_index]['Location']}']['total_monthly_precipitation'][current_month]) / total_yearly_precipitation_local
    
    #Calculates relative yearly precipitation and adds it to the dictionary
    results[f'{items[location_index]['Location']}']['relative_yearly_precipitation'] = total_yearly_precipitation_local / total_yearly_precipitation
        
#Dumps results into json file            
with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, indent=4)