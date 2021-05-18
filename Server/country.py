import json

def read_country_json():
    open_json_file = open('countries.json', 'r')
    read_json_file = open_json_file.read()

    
    allCountry_data = json.loads(read_json_file)

    return allCountry_data

def write_country_json(country_dict):
    country_list = read_country_json()
    country_list.append(country_dict)

    open_json_file = open('countries.json', 'w')
    json.dump(country_list, open_json_file, indent=4)

    return country_dict

def delete_country_json(country_name):
    country_list = read_country_json()
    for item in country_list:
        if item['name']['common'].lower() == country_name.lower():
            country_list.remove(item)
            open_json_file = open('countries.json', 'w')
            json.dump(country_list, open_json_file, indent=4)
            return 200
    return 500

def update_country_json(country_name, new_info):
    country_list = read_country_json()
    if len(new_info) == 0:
        return 500
    for index, item in enumerate(country_list):
        if item['name']['common'].lower() == country_name.lower():
            country_list[index].update(new_info)
            open_json_file = open('countries.json', 'w')
            json.dump(country_list, open_json_file, indent=4)
            return 200
    return 500