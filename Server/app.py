from flask import Flask, request, jsonify, Response
from flask_restx import Api, Resource, fields
from flask_basicauth import BasicAuth
from werkzeug.middleware.proxy_fix import ProxyFix
import country, models, base64, io
from PIL import Image
from models import TFModel


model = TFModel(model_dir='./ml-model/')
model.load()


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

api = Api(app, version='1.0', title='Country API',
          description='Country API',
          )

basic_auth = BasicAuth(app)          


ns_country = api.namespace('Country', description='Country operations')
ns_edit = api.namespace('Countries/<string:country_name>', description='Delete or update')


country_model = api.model('countrySchemas',
    {
        'common_name': fields.String(required=True, description='Common name', example="Thailand"),
        'official_name': fields.String(required=True, description='Official name', example="Kingdom of Thailand"),
        'capital': fields.String(required=True, description='Capital name', example="Bangkok"),
        'region': fields.String(required=True, description='Region Name', example="Asia"),
        'subregion': fields.String(required=True, description='Sub Region Name', example="South-Eastern Asia"),
        'languages': fields.String(required=True, description='Main Languages', example="Thai"),
        'currencies': fields.String(required=True, description='Currencies value', example="THB"),
        'area': fields.Float(required=True, description='Area around the country', example=513120.0),
    }
)

currency_model = api.model('currencySchemas',
    {
        'common_name': fields.String(required=True, description='Common name', example="Thailand"),
        'currencies': fields.String(required=True, description='Currencies value', example="THB"),
    }
)

allCountry_model = api.model('allCountrySchemas',
    {
        'data': fields.String(required=True, description='Common name', example="Thailand"),
        
    }
)

message_model = api.model('Message', {
    "message": fields.String(required=True, description='message alert', example="Country has been edited.")
})

not_found = {
    "common_name": None,
        'official_name': None,
        'capital': None,
        'region': None,
        'subregion': None,
        'languages': None,
        'currencies': None,
        'area': None,
}

#function {ALLDATA}
@ns_country.route('/alldata')
class AllList(Resource):
    #@ns_country.doc('list_of_country')
    #@ns_country.marshal_list_with(allCountry_model, code=200)
    def get(self) -> Response:
        query = request.args.get('query')
        print(query)
        if query != None:
            data = country.read_country_json()
            countries = []
            for item in data:
                if item['name']['common'].lower() == query.lower():
                    countries.append(item)
                    #print(item['name']['common'])
                    response = jsonify({item['name']['common']:countries,"message":"success","status":200})
                    response.status_code = 200
                    return response
            print(countries)
            response = jsonify({"data":None,"message":"Not found","status":204})
            response.status_code = 204
            return response 
        else:
            #1ตัว
            #2ตัว
            x = list()
            for i in country.read_country_json():
            #    x.append({"common":i['name']['common'],"official":i['name']['official']})
               x.append({i['name']['common']:i})
            response = jsonify({"data":x,"message":"success","status":200})
            response.status_code = 200
            return response

    #function {POST:ALLDATA}
    @basic_auth.required
    def post(self):
        return country.write_country_json(api.payload), 200


#function {all}
@ns_country.route('/all')
class CountryList(Resource):
    #@ns_country.doc('list_of_country')
    #@ns_country.marshal_list_with(allCountry_model, code=200)
    def get(self) -> Response:
        query = request.args.get('query')
        print(query)
        if query != None:
            data = country.read_country_json()
            countries = []
            for item in data:
                if item['name']['common'].lower() == query.lower():
                    countries.append({"Common_name":item['name']['common'],"Official_name":item['name']['official']})
                    #print(item['name']['common'])
                    response = jsonify({"data":countries,"message":"success","status":200})
                    response.status_code = 200
                    return response
            print(countries)
            response = jsonify({"data":None,"message":"Not found","status":204})
            response.status_code = 204
            return response 
        else:
            #1ตัว
            #2ตัว
            x = list()
            for i in country.read_country_json():
            #    x.append({"common":i['name']['common'],"official":i['name']['official']})
               x.append({"Common_name":i['name']['common'],"Official_name":i['name']['official']})
            response = jsonify({"data":x,"message":"success","status":200})
            response.status_code = 200
            return response


#function {country}
@ns_country.route('/')
class Country(Resource):
#     @ns_country.doc('list_of_currency')
#     @ns_country.marshal_list_with(currency_model, code=200)
    def get(self) -> Response:
        query = request.args.get('query')
        if query != None:
            data = country.read_country_json()
            result = []
            for item in data:
                 if item['name']['common'].lower() == query.lower():
                    result.append({'common_name':item['name']['common'],
                    'official_name': item['name']['official'], 'capital': item['capital'],
                    'region':item['capital'], 'subregion':item['subregion'], 'languages':item['languages'],
                    'currencies': item['currencies'], 'area': item['area']})
                    #currency.append(item['currencies'])
                    #print(item['currencies'])
                    response = jsonify({"country":result,"message":"success","status":200})
                    response.status_code = 200
                    return response
            print(result)
            response = jsonify({"data":None,"message":"Not found","status":204})
            response.status_code = 204
            return response 
        else:
            #1ตัว
            #2ตัว
            x = list()
            for i in country.read_country_json():
                x.append({'common_name':i['name']['common'],
                    'official_name': i['name']['official'], 'capital': i['capital'],
                    'region': i['capital'], 'subregion': i['subregion'], 'languages':i['languages'],
                    'currencies': i['currencies'], 'area': i['area']})
                #x.append({i['name']['common']:i['name']['official']})
            response = jsonify({"country":x,"message":"success","status":200})
            response.status_code = 200
            return response


#function {countrySchemas}
@ns_country.route('/currency')
class CurrencyList(Resource):
#     @ns_country.doc('Country')
#     @ns_country.marshal_list_with(allCountry_model, code=200)
    def get(self) -> Response:
        query = request.args.get('query')
        if query != None:
            data = country.read_country_json()
            currency = []
            for item in data:
                 if item['name']['common'].lower() == query.lower():
                    currency.append({'Country':item['name']['common'],"Currency":item['currencies']})
                    #currency.append(item['currencies'])
                    #print(item['currencies'])
                    response = jsonify({"data":currency,"message":"success","status":200})
                    response.status_code = 200
                    return response
            print(currency)
            response = jsonify({"data":None,"message":"Not found","status":204})
            response.status_code = 204
            return response 
        else:
            #1ตัว
            #2ตัว
            x = list()
            for i in country.read_country_json():
                x.append({'Country':i['name']['common'],"Currency":i['currencies']})
                #x.append({i['name']['common']:i['name']['official']})
            response = jsonify({"data":x,"message":"success","status":200})
            response.status_code = 200
            return response


#Put&Delete
@ns_edit.route('')
class CountryEdit(Resource):
    #@ns_edit.doc('delete_country')
    #@ns_edit.marshal_with(message_model, code=200)
    @basic_auth.required
    def delete(self, country_name):
        status = country.delete_country_json(country_name)
        if status == 200:
            return {"message":"Country has been deleted."}, 200
        elif status == 500:
            return {"message":country_name+" not found."}, 500

    #@ns_edit.doc('update_country')
    #@ns_edit.marshal_with(message_model, code=200)
    @basic_auth.required
    def put(self, country_name):
        country_dict = api.payload
        status = country.update_country_json(country_name, country_dict)
        if status == 200:
            return {"message":"Food has been updated."}, 200
        elif status == 500:
            return {"message":country_name+" not found."}, 500


@api.route('/ml/country')
class Classification(Resource):
    def post(self):
        image_data = base64.b64decode(api.payload['base64'])

        image_temp = Image.open(io.BytesIO(image_data))

        outputs = model.predict(image_temp)
        return {
            "prediction": outputs['predictions'][0]['label'],
            "confidence": outputs['predictions'][0]['confidence']
            }, 200


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)