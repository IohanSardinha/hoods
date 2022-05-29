
import googlemaps
import json
import time
import sys
import os

API_KEY = os.environ['MAPS_API_KEY']

gmaps = googlemaps.Client(API_KEY)

with open('fixed_zeros.json') as f:
    barrios = json.load(f)
    
    

def addToArray(input, out, bounds, isplayground = False):
    for i in input['results']:
        try:
            geom = i['geometry']['location']
            if bounds is None or (geom['lng'] > bounds['southwest']['lng'] and geom['lng'] < bounds['northeast']['lng'] \
                and geom['lat'] > bounds['southwest']['lat'] and geom['lat'] < bounds['northeast']['lat']):
                out.append(i['rating'])
        except Exception as e:
            print(e)
            continue


final_dict = {}   
    
for b in barrios:
    print(b['Nom_Barri'])
    
    
    gcode = gmaps.geocode(b['Nom_Barri'])
    if len(gcode) > 0:
        gcode = gcode[0]
    else:
        print('nothing returned')
        print(b['Nom_Barri'])
        continue
    try:
        bounds = gcode['geometry']['bounds']
    except:
        bounds = None
    location = gcode['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    
    restaurants = []
    cafes = []
    parks= []
    bars = []
    discos= []
    playgrounds = []
    restaurant = gmaps.places_nearby(location=(lat, lng), radius=700, type='restaurant')
    cafe = gmaps.places_nearby(location=(lat, lng), radius=700, type='cafe')
    park = gmaps.places_nearby(location=(lat, lng), radius=700, type='park')
    bar = gmaps.places_nearby(location=(lat, lng), radius=700, type='bar')
    disco = gmaps.places_nearby(location=(lat, lng), radius=700, type='night_club')
    playground = gmaps.places('playground', location=(lat,lng), radius=700)
    
    addToArray(restaurant ,restaurants, bounds)
    addToArray(cafe ,cafes, bounds)
    addToArray(park ,parks, bounds)
    addToArray(bar ,bars, bounds)
    addToArray(disco ,discos, bounds)
    addToArray(playground ,playgrounds, bounds)
    
    for i in range(1):
        try:
            restaurant = gmaps.places_nearby(page_token=restaurant['next_page_token'])
        except Exception as e:
            #print(e)
            time.sleep(0.5)
        try:
            cafe = gmaps.places_nearby(page_token=cafe['next_page_token'])
        except Exception as e:
            #print(e)
            time.sleep(0.5)
            
        try:
            park = gmaps.places_nearby(page_token=park['next_page_token'])
        except Exception as e:
            #print(e)
            time.sleep(0.5)            
        try:
            bar = gmaps.places_nearby(page_token=bar['next_page_token'])
        except Exception as e:
            #print(e)
            time.sleep(0.5)            
        try:
            disco = gmaps.places_nearby(page_token=disco['next_page_token'])
        except Exception as e:
            #print(e)
            time.sleep(0.5)            
        try:
            playground = gmaps.places(page_token=playground['next_page_token'])
        except Exception as e:
            #print(e)
            time.sleep(0.5)
            
        addToArray(restaurant ,restaurants, bounds)
        addToArray(cafe ,cafes, bounds)
        addToArray(park ,parks, bounds)
        addToArray(bar ,bars, bounds)
        addToArray(disco ,discos, bounds)
        addToArray(playground ,playgrounds, bounds)
        time.sleep(0.5)


        
    final_dict[b['id']] = {
        "restaurants": restaurants,
        "cafes": cafes,
        "parks": parks,
        "bars": bars,
        "discos": discos,
        "playgrounds": playgrounds
    }
    
    
    
with open('ratings.json', "w") as f:
    json.dump(final_dict, f)
