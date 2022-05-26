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

def get_locations(rent_data, locations_factors):
    bars_factor = safe_get(locations_factors, 'bars', 1.0) if "bars_avg" in rent_data[i] else 0
    cafes_factor = safe_get(locations_factors, 'cafes', 1.0) if "cafes_avg" in rent_data[i] else 0
    discos_factor = safe_get(locations_factors, 'discos', 1.0) if "discos_avg" in rent_data[i] else 0
    parks_factor = safe_get(locations_factors, 'parks', 1.0) if "parks_avg" in rent_data[i] else 0
    playgrounds_factor = safe_get(locations_factors, 'playgrounds', 1.0) if "playgrounds_avg" in rent_data[i] else 0
    restaurants_factor = safe_get(locations_factors, 'restaurants', 1.0) if "restaurants_avg" in rent_data[i] else 0
    divisor = bars_factor+cafes_factor+discos_factor+parks_factor+playgrounds_factor+restaurants_factor

    bars_avg = float(rent_data[i]["bars_avg"]) if "bars_avg" in rent_data[i] else 0
    cafes_avg = float(rent_data[i]["cafes_avg"]) if "cafes_avg" in rent_data[i] else 0
    discos_avg = float(rent_data[i]["disco_avg"]) if "discos_avg" in rent_data[i] else 0
    parks_avg = float(rent_data[i]["parks_avg"]) if "parks_avg" in rent_data[i] else 0
    playgrounds_avg = float(rent_data[i]["playg_avg"]) if "playgrounds_avg" in rent_data[i] else 0
    restaurants_avg = float(rent_data[i]["resta_avg"]) if "restaurants_avg" in rent_data[i] else 0

    print(bars_avg)
    print(cafes_avg)
    print(discos_avg)
    print(parks_avg)
    print(playgrounds_avg)
    print(restaurants_avg)


    result = []

    for i in range(n_barris):
        score = (bars_factor * bars_avg + 
                 cafes_factor * cafes_avg +
                 discos_factor * discos_avg +
                 parks_factor * parks_avg +
                 playgrounds_factor * playgrounds_avg +
                 restaurants_factor * restaurants_avg)/divisor

        item = {}
        
        if "bars_num" in rent_data[i]:
            item["bars_num"] = rent_data[i]["bars_num"]
        if "cafes_num" in rent_data[i]:
            item["cafes_num"] = rent_data[i]["cafes_num"]
        if "discos_num" in rent_data[i]:
            item["discos_num"] = rent_data[i]["discos_num"]
        if "parks_num" in rent_data[i]:
            item["parks_num"] = rent_data[i]["parks_num"]
        if "playgrounds_num" in rent_data[i]:
            item["playgrounds_num"] = rent_data[i]["playgrounds_num"]
        if "restaurants_num" in rent_data[i]:
            item["restaurants_num"] = rent_data[i]["restaurants_num"]
        item["score"] = score

        result.append(item)

    return result



def compute_score(price, distance, locations):

    price_factor = 1.0
    distance_factor = 1.0
    locations_factor = 0.0

    divisor = 2.0

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
