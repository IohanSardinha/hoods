import json
import requests
import urllib.parse

n_barris = 73

def get_prices(rent_data):

    valid_prices = [rent_data[str(i)]['Preu'] for i in range(n_barris) if not rent_data[str(i)]['Preu'] == None]

    min_price = min(valid_prices)
    max_price = max(valid_prices)

    results = []

    for i in range(n_barris):
        score = 0.5
        price = rent_data[str(i)]['Preu']
        if price != None:
            score = 5*( 1 - (price - min_price)/(max_price - min_price)) 

        results.append(score)

    return results

def get_distances(origin, rent_data, max_commute_time=60):
    API_KEY = "AIzaSyBqmA-bUOGcjvdsa38whNoiIb0oUBr5IpE"

    origins_list = [origin]
    origins = urllib.parse.quote("|".join(origins_list))

            
    destinations_list = [rent_data[str(i)]['Nom_Barri'] for i in range(n_barris)]

    responses = []

    for i in range(0, n_barris, 25):
        
        destinations = urllib.parse.quote("|".join( destinations_list[i:(i+25)] ))

        url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+origins+"&destinations="+destinations+"&units=meters&key="+API_KEY

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        
        responses += json.loads(response.text)["rows"][0]["elements"]

    result = []
    for response in responses:
        score = 0
        if response['status'] == "OK" and response['duration']['value'] < max_commute_time:
            score = 5 * (1-response['duration']['value']/max_commute_time)
            
        result.append(score)
    
    return result

def get_locations():
    return [2.5 for i in range(n_barris)]


def compute_score(price, distance, locations):

    price_factor = 1.0
    distance_factor = 1.0
    locations_factor = 0.0

    divisor = 2.0

    return (price * price_factor + distance * distance_factor + locations * locations_factor)/divisor

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


print(json.dumps(lambda_handler({'origin':'Microsoft Iberica barcelona'}, None), indent=4))