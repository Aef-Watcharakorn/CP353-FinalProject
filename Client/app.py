from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json

app = Flask(__name__)

currency_api = "http://localhost:8000/Country/currency"
country_api = "http://localhost:8000/Country/?query={0}"

#OPEN_WEATHER_KEY = '456c1a3c436150042b033dd0e6261e4a'

@app.route("/currency")
def currency():
    currency = request.args.get('query')
    data = get_currency(currency_api)
    return render_template("currency.html", data=data)

@app.route("/")
def index():
    country = request.args.get('query')
    if not country:
        country = 'thailand'
    data = get_country(country,country_api)
    return render_template("index.html", data=data)


def get_currency(API):
    url =  API    
    data = urlopen(url).read()      
    parsed = json.loads(data)
    country = []
    currency = []
    for i in parsed:
        country.append(parsed['data'][i]['Country'])
    # for i in parsed:
    #     country.append(parsed['data'][i]['Currency'][0])
    result = {'country': country,
                   'currency': currency
                   }
    return result

def get_country(country,API):
    query = quote(country)
    url = API.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    country = None       

    common_name = parsed['country'][0]['common_name']
    official_name = parsed['country'][0]['official_name']
    currencies = parsed['country'][0]['currencies']
    area = parsed['country'][0]['area']
    capital = parsed['country'][0]['capital'][0]
    region = parsed['country'][0]['region'][0]
    subregion = parsed['country'][0]['subregion']
    languages = parsed['country'][0]['languages']
    lan = []
    cur = []
    for i in languages:
        lan.append(i)
    for i in currencies:
        cur.append(i)


    country = {'common_name': common_name,
                'official_name': official_name,
                'currencies': cur[0],
                'area': area,
                'capital': capital,
                'region': region,
                'subregion': subregion,
                'languages': lan[0],
                }
    return country
