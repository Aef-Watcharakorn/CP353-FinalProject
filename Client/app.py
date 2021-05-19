from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json, base64, requests

app = Flask(__name__)

currency_api = "http://localhost:8000/Country/currency"
country_api = "http://localhost:8000/Country/?query={0}"

#OPEN_WEATHER_KEY = '456c1a3c436150042b033dd0e6261e4a'

@app.route("/currency")
def currency():
    currency = request.args.get('query')
    data = get_currency(currency_api)
    return render_template("currency.html", data=data, total=len(data['country']))

@app.route("/")
def index():
    country = request.args.get('query')
    if not country:
        country = 'thailand'
    data = get_country(country,country_api)
    return render_template("index.html", data=data)

@app.route('/service', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file in form!'
        file1 = request.files['file1']

        base64_encoded_data = base64.b64encode(file1.read())
        base64_message = base64_encoded_data.decode('utf-8')

        url = "http://localhost:8000/ml/country"
        body = {
            'base64' : base64_message
            }
        prediction = requests.post(url, json = body)
        url = prediction.json()['prediction']

        return render_template('service.html', url=url)
    return render_template('service.html')


def get_currency(API):
    url =  API    
    data = urlopen(url).read()      
    parsed = json.loads(data)
    country = []
    currency = []
    for i in parsed['data']:
        try :
            currency.append(list(i['Currency'].keys())[0])
            country.append(i['Country'])
            #print(list(i['Currency'].keys())[0])
        except :
            currency.append("")
            country.append(i['Country'])
    
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
