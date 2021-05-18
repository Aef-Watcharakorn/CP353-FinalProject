import json
open_json_file = open('countries.json', 'r')
read_json_file = open_json_file.read()

    
allCountry_data = json.loads(read_json_file)

countries = []
for item in allCountry_data:
    datatest = item['name']['common'].lower()
    countries.append(datatest)

print(countries)