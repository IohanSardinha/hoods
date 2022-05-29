import json
from datetime import datetime
import requests
import urllib.parse
import boto3
from boto3.dynamodb.conditions import Key
import base64
from botocore.exceptions import ClientError

client = boto3.client('secretsmanager')
response = client.get_secret_value(
    SecretId='MAPS_API_KEY'
)

MAPS_API_KEY = response['SecretString']
TABLE_NAME = "hoods_rent_prices"

# Creating the DynamoDB Client
# dynamodb_client = boto3.client('dynamodb', region_name="eu-west-1")

# Creating the DynamoDB Table Resource
dynamodb = boto3.resource('dynamodb', region_name="eu-west-1")
table = dynamodb.Table(TABLE_NAME)

n_barris = 73

def get_prices(rent_data, min_price = None, max_price = None):

    valid_prices = [float(rent_data[i]['Preu']['y2021']) for i in range(n_barris) if not rent_data[i]['Preu']['y2021'] == None]

    avg_price = sum(valid_prices)/len(valid_prices)
    deviation = avg_price/2.5
    min_price = min_price or avg_price-deviation
    max_price = max_price or avg_price+deviation

    results = []

    for i in range(n_barris):
        score = 2.5
        price = float(rent_data[i]['Preu']['y2021'])
        if price != None:
            score = 5*(1 - (price - min_price)/(max_price - min_price)) 

        results.append({
            "nom_barri":rent_data[i]['Nom_Barri'],
            # "rent":(price if price != None else "not found"),
            "score": max(min(score,5),0)
        })
    
    return results

def get_results_by_mode(MAPS_API_KEY,origins,destinations_list, max_commute_time, min_commute_time , mode):
    responses = []

    for i in range(0, n_barris, 25):
        
        destinations = urllib.parse.quote("|".join( destinations_list[i:(i+25)] ))

        url = "https://maps.googleapis.com/maps/api/distancematrix/json?mode="+mode+"&origins="+origins+"&destinations="+destinations+"&units=meters&key="+MAPS_API_KEY

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        responses += json.loads(response.text)["rows"][0]["elements"]


    result = []
    for response in responses:
        score = 0
        if response['status'] == "OK" and response['duration']['value']/60 < max_commute_time:
            time_in_mins = response['duration']['value']/60
            score = 5 * (1-(time_in_mins-min_commute_time)/max_commute_time)
            
        result.append({
            "mode":"public transport" if mode == 'transit' else mode,
            "duration_value":response['duration']['value']/60 if response['status'] == "OK" else "Not found",
            "duration": (response['duration']['text'] if response['status'] == "OK" else "Could not find") ,
            "score":max(min(score,5),0)
        })

    return result


def get_distances(origin, rent_data, min_commute_time = 10, max_commute_time=60):

    origins_list = [origin]
    origins = urllib.parse.quote("|".join(origins_list))

    
    destinations_list = [str(rent_data[i]['center']["lat"])+","+str(rent_data[i]['center']["lng"]) for i in range(n_barris)]

    #destinations_list = [rent_data[i]['Nom_Barri'] for i in range(n_barris)]

    result_transit = get_results_by_mode(MAPS_API_KEY,origins,destinations_list, max_commute_time, min_commute_time , 'transit')

    result_walking = get_results_by_mode(MAPS_API_KEY,origins,destinations_list, max_commute_time, min_commute_time , 'walking')

    results = []

    for transit, walking in zip(result_transit, result_walking):
        if(walking['score'] >= transit['score']):
            results.append(walking)
        else:
            results.append(transit)
    
    return results

def get_locations(rent_data, locations_factors={}):
    
    result = []

    for i in range(n_barris):
        bars_factor = safe_get(locations_factors, 'bars', 1.0) if "bars_avg" in rent_data[i] else 0
        cafes_factor = safe_get(locations_factors, 'cafes', 1.0) if "cafes_avg" in rent_data[i] else 0
        discos_factor = safe_get(locations_factors, 'discos', 1.0) if "discos_avg" in rent_data[i] else 0
        parks_factor = safe_get(locations_factors, 'parks', 1.0) if "parks_avg" in rent_data[i] else 0
        playgrounds_factor = safe_get(locations_factors, 'playgrounds', 1.0) if "playgrounds_avg" in rent_data[i] else 0
        restaurants_factor = safe_get(locations_factors, 'restaurants', 1.0) if "restaurants_avg" in rent_data[i] else 0
        divisor = bars_factor+cafes_factor+discos_factor+parks_factor+playgrounds_factor+restaurants_factor
    
        bars_avg = float(rent_data[i]["bars_avg"]) if "bars_avg" in rent_data[i] else 0
        cafes_avg = float(rent_data[i]["cafes_avg"]) if "cafes_avg" in rent_data[i] else 0
        discos_avg = float(rent_data[i]["discos_avg"]) if "discos_avg" in rent_data[i] else 0
        parks_avg = float(rent_data[i]["parks_avg"]) if "parks_avg" in rent_data[i] else 0
        playgrounds_avg = float(rent_data[i]["playgrounds_avg"]) if "playgrounds_avg" in rent_data[i] else 0
        restaurants_avg = float(rent_data[i]["restaurants_avg"]) if "restaurants_avg" in rent_data[i] else 0
        
        score = 0
        item = {}
        
        if divisor != 0:
            score = (bars_factor * bars_avg + 
                     cafes_factor * cafes_avg +
                     discos_factor * discos_avg +
                     parks_factor * parks_avg +
                     playgrounds_factor * playgrounds_avg +
                     restaurants_factor * restaurants_avg)/divisor


        item["score"] = min(max(score,0),5)

        result.append(item)

    return result


def compute_score(price, distance, locations, any_location):

    price_factor = 1.0
    distance_factor = 1.0
    locations_factor = 1.0 if any_location else 0.0

    divisor = price_factor+distance_factor+locations_factor

    score = (price['score'] * price_factor + distance['score'] * distance_factor + locations['score'] * locations_factor)/divisor 

    not_score = lambda tup: tup[0] != 'score'

    price_items = filter(not_score ,price.items())
    distance_items = filter(not_score ,distance.items())
    locations_items = filter(not_score ,locations.items())

    ret = {k:v for (k,v) in list(price_items) + list(distance_items) + list(locations_items)}
    ret['score'] = score


    return ret


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET'
            },
    }
    
def safe_get(_dict,field, default=None):
    return _dict[field] if field in _dict else default
        
    
def lambda_handler(event, context):
    
        
    operation = event['httpMethod']
    if operation == 'GET':
        commute_location = event['queryStringParameters']['origin']
        
        max_commute_time = safe_get(event['queryStringParameters'],'max_commute_time',60)
        if max_commute_time == "":
            max_commute_time = 60
        
        locations_factors = {}
        #restaurants
        is_restaurants = safe_get(event['queryStringParameters'],'restaurants', False)
        if is_restaurants:
            locations_factors['restaurants'] = 1
            locations_factors['cafes'] = 1
        else:
            locations_factors['restaurants'] = 0
            locations_factors['cafes'] = 0

        #parks
        is_parks = safe_get(event['queryStringParameters'],'parks', False)
        if is_parks:
            locations_factors['parks'] = 1
            locations_factors['playgrounds'] = 1
        else:
            locations_factors['parks'] = 0
            locations_factors['playgrounds'] = 0
        
        #bars
        is_bars = safe_get(event['queryStringParameters'],'bars', False)
        if is_bars:
            locations_factors['bars'] = 1
            locations_factors['discos'] = 1
        else:
            locations_factors['bars'] = 0
            locations_factors['discos'] = 0
    
        result = table.scan()
        rent_data = sorted(result["Items"], key=lambda item: item["id"])
    
        #Getting the different parameters
        prices = get_prices(rent_data, safe_get(event['queryStringParameters'],'min_price'), safe_get(event['queryStringParameters'],'max_price'))
        
        distances = get_distances(commute_location, rent_data, safe_get(event['queryStringParameters'],'min_commute_time', 10), int(max_commute_time))
        
        locations = get_locations(rent_data, locations_factors)

        #Computing the score
        scores = [compute_score(prices[i], distances[i], locations[i], is_bars or is_parks or is_restaurants) for i in range(n_barris)]
    
        return {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET'
            },
            "body": json.dumps(scores,indent=4)
        }
        
    else: 
        return {
        'statusCode': 400,
        'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET'
            },
        'body': json.dumps(str(ValueError('Unsupported method %s'%operation)))
    }