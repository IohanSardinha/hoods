import json
import requests
import urllib.parse

def main():
	from datetime import datetime
	import googlemaps
	
	gmaps = googlemaps.Client(key='AIzaSyBqmA-bUOGcjvdsa38whNoiIb0oUBr5IpE')

	aux = []
	aux2 = []
	f = open('data/rent_data.json')
	data = json.load(f)
	for i in data:
		if data[i]['Nom_Districte'] == 'GrÃ cia':
			data[i]['Nom_Districte'] = 'Gracia Barcelona'

		aux.append(data[i]['Nom_Districte'])

	for i in data:
		aux2.append(data[i]['Nom_Barri'])

	origin = list(set(aux))
	origin2 = list(set(aux2))

	# keeping the following prints only for the POC
	print(origin2)
	print(len(origin2))
	# ['Sants', 'Vallcarca i els Penitents', "la Vall d'Hebron", 'el Bon Pastor', 'el GuinardÃ³', 'el Fort Pienc', 'la Salut', 'Pedralbes', 'la Marina de Port', 'Can Peguera', 'la Vila de Gràcia', 'la Verneda i la Pau', 'el Congrés i els Indians', 'la Prosperitat', 'Sarrià', 'Torre BarÃ³', 'la Guineueta', 'Vallbona', 'Baró de Viver', 'les Roquetes', 'la Font de la Guatlla', 'BarÃ³ de Viver', 'Ciutat Meridiana', 'Sant Genís dels Agudells', 'el Raval', "el Camp d'en Grassot i GrÃ cia Nova", 'la Vila Olímpica del Poblenou', 'Navas', 'el Guinardó', "la Font d'en Fargues", 'Torre Baró', 'Horta', 'el BesÃ²s i el Maresme', 'Verdun', 'Sant Andreu', 'el Baix Guinardó', 'Sant Antoni', "la Nova Esquerra de l'Eixample", 'la Clota', 'el Putxet i el FarrÃ³', 'ProvenÃ§als del Poblenou', 'el Barri GÃ²tic', 'Sant Gervasi - Galvany', 'la Teixonera', 'la Sagrera', "la Dreta de l'Eixample", 'Can Baró', 'Can BarÃ³', 'el Parc i la Llacuna del Poblenou', 'Sant Gervasi - la Bonanova', 'la Sagrada FamÃ\xadlia', 'el TurÃ³ de la Peira', 'SarriÃ ', 'la Bordeta', 'el Besòs i el Maresme', 'el Poble Sec', 'Vallvidrera, el Tibidabo i les Planes', 'Montbau', 'el Putxet i el Farró', 'Vilapicina i la Torre Llobeta', 'Sant Martí de Provençals', 'Provençals del Poblenou', 'la Marina del Prat Vermell', 'Sant GenÃ\xads dels Agudells', 'la Barceloneta', "el Camp de l'Arpa del Clot", 'la Vila OlÃ\xadmpica del Poblenou', 'les Tres Torres', 'la Vila de GrÃ cia', 'Hostafrancs', 'el Carmel', 'Sant Pere, Santa Caterina i la Ribera', 'Diagonal Mar i el Front MarÃ\xadtim del Poblenou', 'el Baix GuinardÃ³', "el Camp d'en Grassot i Gràcia Nova", 'la Trinitat Vella', 'la Maternitat i Sant Ramon', 'Canyelles', 'Diagonal Mar i el Front Marítim del Poblenou', 'el Turó de la Peira', 'Sant MartÃ\xad de ProvenÃ§als', "l'Antiga Esquerra de l'Eixample", 'el CongrÃ©s i els Indians', 'la Trinitat Nova', 'el Poblenou', 'les Corts', 'el Clot', 'el Coll', 'el Barri Gòtic', 'Porta', 'la Sagrada Família', 'Sants - Badal']
	# 92

	print(origin)
	print(len(origin))
	# ['Ciutat Vella', 'Les Corts', 'Sant Andreu', 'Sants-Montjuïc', 'Sant Martí', 'Eixample', 'Sants-MontjuÃ¯c', 'Gracia Barcelona', 'Nou Barris', 'Sant MartÃ\xad', 'SarriÃ -Sant Gervasi', 'Sarrià-Sant Gervasi', 'Horta-GuinardÃ³', 'Gràcia', 'Horta-Guinardó']
	# 15


	dest = ['Microsoft Iberica barcelona']

	now = datetime.now()
	directions_result = gmaps.distance_matrix(origin,
											dest,
											mode="walking",
											departure_time=now)

	json_str = json.dumps(directions_result, indent=2)
	print(json_str)



API_KEY = "AIzaSyBqmA-bUOGcjvdsa38whNoiIb0oUBr5IpE"

origins_list = ["Microsoft Iberica barcelona"]
origins = urllib.parse.quote("|".join(origins_list))

with open('data/rent_data.json') as raw_data:
	rent_data = json.load(raw_data)
        
	destinations_list = [rent_data[str(i)]['Nom_Barri'] for i in range(73)]

responses = []

for i in range(0, 73, 25):
	
	destinations = urllib.parse.quote("|".join( destinations_list[i:(i+25)] ))

	url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+origins+"&destinations="+destinations+"&units=meters&key="+API_KEY

	payload={}
	headers = {}

	response = requests.request("GET", url, headers=headers, data=payload)
	
	responses += json.loads(response.text)["rows"][0]["elements"]

result = []
for response in responses:
	if response['status'] == "OK":
		result.append(response['duration']['value'])
	else:
		result.append(-1)

print(result)