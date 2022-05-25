import json
import requests
import urllib.parse

n_barris = 73

def get_prices(rent_data, min_price = None, max_price = None):

    valid_prices = [rent_data[str(i)]['Preu'] for i in range(n_barris) if not rent_data[str(i)]['Preu'] == None]

    avg_price = sum(valid_prices)/len(valid_prices)
    deviation = avg_price/2.5
    min_price = min_price or avg_price-deviation
    max_price = max_price or avg_price+deviation

    results = []

    for i in range(n_barris):
        score = 2.5
        price = rent_data[str(i)]['Preu']
        if price != None:
            score = 5*(1 - (price - min_price)/(max_price - min_price)) 

        results.append({
            "rent":(price if price != None else "not found"),
            "score": max(min(score,5),0)
        })
    
    return results

def get_results_by_mode(API_KEY,origins,destinations_list, max_commute_time, min_commute_time , mode):
    responses = []

    for i in range(0, n_barris, 25):
        
        destinations = urllib.parse.quote("|".join( destinations_list[i:(i+25)] ))

        url = "https://maps.googleapis.com/maps/api/distancematrix/json?mode="+mode+"&origins="+origins+"&destinations="+destinations+"&units=meters&key="+API_KEY

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
            "durantion": (response['duration']['text'] if response['status'] == "OK" else "Could not find") ,
            "score":max(min(score,5),0)
        })

    return result


def get_distances(origin, rent_data, min_commute_time = 10, max_commute_time=60):
    API_KEY = "AIzaSyBqmA-bUOGcjvdsa38whNoiIb0oUBr5IpE"

    origins_list = [origin]
    origins = urllib.parse.quote("|".join(origins_list))

            
    destinations_list = [rent_data[str(i)]['Nom_Barri'] for i in range(n_barris)]

    result_transit = get_results_by_mode(API_KEY,origins,destinations_list, max_commute_time, min_commute_time , 'transit')

    result_walking = get_results_by_mode(API_KEY,origins,destinations_list, max_commute_time, min_commute_time , 'walking')

    results = []

    for transit, walking in zip(result_transit, result_walking):
        if(walking['score'] >= transit['score']):
            results.append(walking)
        else:
            results.append(transit)
    
    return results

def get_locations():
    return [{'score':2.5} for _ in range(n_barris)]


def compute_score(price, distance, locations):

    price_factor = 0.0
    distance_factor = 1.0
    locations_factor = 0.0

    divisor = 1.0

    score = (price['score'] * price_factor + distance['score'] * distance_factor + locations['score'] * locations_factor)/divisor 

    not_score = lambda tup: tup[0] != 'score'

    price_items = filter(not_score ,price.items())
    distance_items = filter(not_score ,distance.items())
    locations_items = filter(not_score ,locations.items())

    ret = {k:v for (k,v) in list(price_items) + list(distance_items) + list(locations_items)}
    ret['score'] = score


    return ret

def lambda_handler(event, context):

    #Getting the request data

    commute_location = event['origin']

    with open('data/rent_data.json') as raw_data:
        rent_data = json.load(raw_data)

        #Getting the different parameters
        prices = get_prices(rent_data)
        
        distances = get_distances(commute_location, rent_data)

        locations = get_locations()


    #Computing the score
    scores = [compute_score(prices[i], distances[i], locations[i]) for i in range(n_barris)]

    return {
        "statusCode": 200,
        "body": scores
    }


print(json.dumps(lambda_handler({'origin':'El Raval'}, None), indent=4))
