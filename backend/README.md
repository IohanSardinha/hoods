# Backend
This folder contains the scripts that are implemented as Lambda functions and connected to API Gateways to work as the backend

## Requirements
To use this scripts, first run:
```bash
$ pip install -r requirements.txt 
```

## hoods_get_barrio_lambda.py
Script with the implementation of the lambda function that receives an barrio id and returns it's information
#### Example request:
```json
{
    "httpMethod": "GET",
    "queryStringParameters":{
        "id":"int - the barrio id"
    }
}
```
#### Example response:
```json
{
  "statusCode": 200,
  "headers": {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET"
  },
  "body": {
    "cafes_avg": 3.825,
    "discos_num": 8,
    "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Poble_Sec_capvespre.jpg/300px-Poble_Sec_capvespre.jpg",
    "playgrounds_num": 6,
    "Codi_Districte": 3,
    "parks_num": 19,
    "Preu": {
      "y2020": 865.8,
      "y2021": 856.2,
      "y2014": 602.55,
      "y2015": 602.55,
      "y2016": 638.47,
      "y2017": 706.11,
      "y2018": 760.23,
      "y2019": 822.04
    },
    "bars_avg": 4.053846153846154,
    "discos_avg": 4.275,
    "Nom_Barri": "el Poble Sec",
    "center": {
      "lng": 2.166704790476191,
      "lat": 41.373081357142865
    },
    "restaurants_avg": 4.196153846153846,
    "parks_avg": 4.342105263157895,
    "Nom_Districte": "Sants-Montjuïc",
    "cafes_num": 8,
    "bars_num": 26,
    "playgrounds_avg": 3.3833333333333333,
    "PreuM2": {
      "y2020": 865.8,
      "y2021": 856.2,
      "y2014": 602.55,
      "y2015": 602.55,
      "y2016": 638.47,
      "y2017": 706.11,
      "y2018": 760.23,
      "y2019": 822.04
    },
    "restaurants_num": 26,
    "description": "El Poble-sec  ( pronounced  [əl ˌpɔbːləˈsɛk] ;  Catalan  for ''Dry village'') is a neighborhood in the  Sants-Montjuïc  district of  Barcelona ,  Catalonia  ( Spain ).  The neighborhood is located between  Montjuïc  mountain and the  Avinguda del Paral·lel .  ",
    "id": 10,
    "news": [
      {
        "title": "Más de 120 entidades en las calles",
        "date": "24/05/2022 - 21:30",
        "url": "https://ajuntament.barcelona.cat/sants-montjuic/es/noticia/firentitats-sans-hostafrancs-bordeta-secretariado-calle-creu-coberta-cotxeres-espana-industrial_1178977"
      },
      {
        "title": "Obras de mejora en los andenes de la estación de Sants",
        "date": "11/05/2022 - 19:05",
        "url": "https://ajuntament.barcelona.cat/sants-montjuic/es/noticia/obras-de-mejora-en-los-andenes-de-la-estacion-de-sants_1177260"
      },
      {
        "title": "Publicada la Resolución provisional de la Convocatoria General de Subvención 2022",
        "date": "27/05/2022 - 12:06",
        "url": "https://ajuntament.barcelona.cat/sants-montjuic/es/noticia/publicada-la-resolucion-provisional-de-la-convocatoria-general-de-subvencion-2022_1179645"
      },
      {
        "title": "Se cierra el período de preinscripción en las escoles bressol municipales",
        "date": "26/05/2022 - 08:50",
        "url": "https://ajuntament.barcelona.cat/sants-montjuic/es/noticia/se-cierra-el-periodo-de-preinscripcion-en-las-escoles-bressol-municipales_1178877"
      }
    ]
  }
}
```

## hoods_score_lambda.py
Script with the implementation of the lambda function that receives an barrio a commute location and user preferences and returns the scores for all barrios
Parameters between brackets are optional
#### Example request:
```json
{
    "httpMethod": "GET",
    "queryStringParameters":{
        "origin":"string: commute location",
        "[min_price]":"float - minumum rent price; Default= min_price_in_db - avg_price_in_db/2.5",
        "[max_price]":"float - maximun rent price; Default= min_price_in_db + avg_price_in_db/2.5",
        "[min_commute_time]":"float - minumim commute time in minutes; Default 10",
        "[max_commute_time]":"float - maximun commute time in minutes; Default 60",       
        "[bars]": "float - the weight for this locations, between 0 and 1; Default= 1", 
        "[parks]": "float - the weight for this locations, between 0 and 1; Default= 1", 
        "[restaurants]": "float - the weight for this locations, between 0 and 1; Default= 1" 
    }
}
```
#### Example response:
```json
{
  "statusCode": 200,
  "headers": {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET"
  },
  "body": [
    {
      "nom_barri": "el Raval",
      "mode": "public transport",
      "duration_value": 33.06666666666667,
      "duration": "33 mins",
      "score": 2.973999635206762
    },
    {
      "nom_barri": "el Barri Gótic",
      "mode": "public transport",
      "duration_value": 28.666666666666668,
      "duration": "29 mins",
      "score": 2.3217854964409645
    },
    {
      "nom_barri": "la Barceloneta",
      "mode": "public transport",
      "duration_value": 30.283333333333335,
      "duration": "30 mins",
      "score": 2.970948001004607
    },
    {
      "nom_barri": "Sant Pere, Santa Caterina i la Ribera",
      "mode": "public transport",
      "duration_value": 31.5,
      "duration": "32 mins",
      "score": 2.4764646061778395
    },
    {
      "nom_barri": "el Fort Pienc",
      "mode": "public transport",
      "duration_value": 23.933333333333334,
      "duration": "24 mins",
      "score": 2.690062003753078
    },
    {
      "nom_barri": "la Sagrada Família",
      "mode": "public transport",
      "duration_value": 31.883333333333333,
      "duration": "32 mins",
      "score": 2.654331235846747
    },
    {
      "nom_barri": "la Dreta de l'Eixample",
      "mode": "public transport",
      "duration_value": 27.6,
      "duration": "28 mins",
      "score": 1.7666666666666666
    },
    {
      "nom_barri": "l'Antiga Esquerra de l'Eixample",
      "mode": "public transport",
      "duration_value": 49.25,
      "duration": "49 mins",
      "score": 1.1849506471966071
    },
    {
      "nom_barri": "la Nova Esquerra de l'Eixample",
      "mode": "public transport",
      "duration_value": 45.7,
      "duration": "46 mins",
      "score": 1.757612447217695
    },
    {
      "nom_barri": "Sant Antoni",
      "mode": "public transport",
      "duration_value": 46.9,
      "duration": "47 mins",
      "score": 1.9011112309476124
    },
    {
      "nom_barri": "el Poble Sec",
      "mode": "public transport",
      "duration_value": 40.96666666666667,
      "duration": "41 mins",
      "score": 2.673058625920733
    },
    {
      "nom_barri": "la Marina del Prat Vermell",
      "mode": "walking",
      "duration_value": 129.9,
      "duration": "2 hours 10 mins",
      "score": 2.5
    },
    {
      "nom_barri": "la Marina de Port",
      "mode": "walking",
      "duration_value": 116.53333333333333,
      "duration": "1 hour 57 mins",
      "score": 1.5585554888380133
    },
    {
      "nom_barri": "la Font de la Guatlla",
      "mode": "public transport",
      "duration_value": 46.4,
      "duration": "46 mins",
      "score": 2.3575718787941677
    },
    {
      "nom_barri": "Hostafrancs",
      "mode": "public transport",
      "duration_value": 35.95,
      "duration": "36 mins",
      "score": 2.84263849699786
    },
    {
      "nom_barri": "la Bordeta",
      "mode": "public transport",
      "duration_value": 45.36666666666667,
      "duration": "45 mins",
      "score": 2.3625398002939226
    },
    {
      "nom_barri": "Sants - Badal",
      "mode": "public transport",
      "duration_value": 52.85,
      "duration": "53 mins",
      "score": 2.170778305646382
    },
    {
      "nom_barri": "Sants",
      "mode": "public transport",
      "duration_value": 38.55,
      "duration": "39 mins",
      "score": 2.654049077618376
    },
    {
      "nom_barri": "les Corts",
      "mode": "walking",
      "duration_value": 100.55,
      "duration": "1 hour 41 mins",
      "score": 0.6458125441436438
    },
    {
      "nom_barri": "la Maternitat i Sant Ramon",
      "mode": "walking",
      "duration_value": 123.36666666666666,
      "duration": "2 hours 3 mins",
      "score": 0.9321499358845747
    },
    {
      "nom_barri": "Pedralbes",
      "mode": "walking",
      "duration_value": 129.68333333333334,
      "duration": "2 hours 10 mins",
      "score": 0
    },
    {
      "nom_barri": "Vallvidrera, el Tibidabo i les Planes",
      "mode": "walking",
      "duration_value": 186.25,
      "duration": "3 hours 6 mins",
      "score": 0
    },
    {
      "nom_barri": "Sarrià",
      "mode": "walking",
      "duration_value": 129.73333333333332,
      "duration": "2 hours 10 mins",
      "score": 0
    },
    {
      "nom_barri": "les Tres Torres",
      "mode": "public transport",
      "duration_value": 55.7,
      "duration": "56 mins",
      "score": 0.5958333333333332
    },
    {
      "nom_barri": "Sant Gervasi - la Bonanova",
      "mode": "walking",
      "duration_value": 126.41666666666667,
      "duration": "2 hours 6 mins",
      "score": 0
    },
    {
      "nom_barri": "Sant Gervasi - Galvany",
      "mode": "public transport",
      "duration_value": 47.21666666666667,
      "duration": "47 mins",
      "score": 0.9493055555555554
    },
    {
      "nom_barri": "el Putxet i el Farrï",
      "mode": "public transport",
      "duration_value": 47.21666666666667,
      "duration": "47 mins",
      "score": 1.6740139131005
    },
    {
      "nom_barri": "Vallcarca i els Penitents",
      "mode": "public transport",
      "duration_value": 44.63333333333333,
      "duration": "45 mins",
      "score": 1.825521594785803
    },
    {
      "nom_barri": "el Coll",
      "mode": "public transport",
      "duration_value": 55.416666666666664,
      "duration": "55 mins",
      "score": 1.8869984173714336
    },
    {
      "nom_barri": "la Salut",
      "mode": "public transport",
      "duration_value": 44.333333333333336,
      "duration": "44 mins",
      "score": 2.0396820143848196
    },
    {
      "nom_barri": "la Vila de Gràcia",
      "mode": "public transport",
      "duration_value": 37.15,
      "duration": "37 mins",
      "score": 2.4668531985562785
    },
    {
      "nom_barri": "el Camp d'en Grassot i Gràcia Nova",
      "mode": "public transport",
      "duration_value": 30.783333333333335,
      "duration": "31 mins",
      "score": 2.714787500112218
    },
    {
      "nom_barri": "el Baix Guinardï",
      "mode": "public transport",
      "duration_value": 31.716666666666665,
      "duration": "32 mins",
      "score": 2.838791260444121
    },
    {
      "nom_barri": "Can Barï",
      "mode": "public transport",
      "duration_value": 45.266666666666666,
      "duration": "45 mins",
      "score": 2.5200772076674296
    },
    {
      "nom_barri": "el Guinardï",
      "mode": "public transport",
      "duration_value": 49.95,
      "duration": "50 mins",
      "score": 2.2844702075942527
    },
    {
      "nom_barri": "la Font d'en Fargues",
      "mode": "public transport",
      "duration_value": 42.93333333333333,
      "duration": "43 mins",
      "score": 2.111278006005441
    },
    {
      "nom_barri": "el Carmel",
      "mode": "public transport",
      "duration_value": 50.11666666666667,
      "duration": "50 mins",
      "score": 2.796129708998882
    },
    {
      "nom_barri": "la Teixonera",
      "mode": "public transport",
      "duration_value": 47.61666666666667,
      "duration": "48 mins",
      "score": 2.762228702213271
    },
    {
      "nom_barri": "Sant Genís dels Agudells",
      "mode": "public transport",
      "duration_value": 59.05,
      "duration": "59 mins",
      "score": 2.1402906403254285
    },
    {
      "nom_barri": "Montbau",
      "mode": "walking",
      "duration_value": 106.86666666666666,
      "duration": "1 hour 47 mins",
      "score": 1.6602358690405534
    },
    {
      "nom_barri": "la Vall d'Hebron",
      "mode": "public transport",
      "duration_value": 53.75,
      "duration": "54 mins",
      "score": 1.775866668212037
    },
    {
      "nom_barri": "la Clota",
      "mode": "public transport",
      "duration_value": 50.833333333333336,
      "duration": "51 mins",
      "score": 3.298611111111111
    },
    {
      "nom_barri": "Horta",
      "mode": "public transport",
      "duration_value": 52.15,
      "duration": "52 mins",
      "score": 2.3448140089895766
    },
    {
      "nom_barri": "Vilapicina i la Torre Llobeta",
      "mode": "public transport",
      "duration_value": 37.6,
      "duration": "38 mins",
      "score": 2.8616260825906874
    },
    {
      "nom_barri": "Porta",
      "mode": "public transport",
      "duration_value": 35.3,
      "duration": "35 mins",
      "score": 3.2386957852467644
    },
    {
      "nom_barri": "el Turï de la Peira",
      "mode": "public transport",
      "duration_value": 46.083333333333336,
      "duration": "46 mins",
      "score": 2.9186161309519614
    },
    {
      "nom_barri": "Can Peguera",
      "mode": "public transport",
      "duration_value": 42.75,
      "duration": "43 mins",
      "score": 3.635416666666667
    },
    {
      "nom_barri": "la Guineueta",
      "mode": "public transport",
      "duration_value": 43.983333333333334,
      "duration": "44 mins",
      "score": 2.835741982184495
    },
    {
      "nom_barri": "Canyelles",
      "mode": "walking",
      "duration_value": 103.98333333333333,
      "duration": "1 hour 44 mins",
      "score": 1.5412120126161755
    },
    {
      "nom_barri": "les Roquetes",
      "mode": "public transport",
      "duration_value": 49.05,
      "duration": "49 mins",
      "score": 3.033052732689606
    },
    {
      "nom_barri": "Verdun",
      "mode": "public transport",
      "duration_value": 44.36666666666667,
      "duration": "44 mins",
      "score": 3.0891037436425792
    },
    {
      "nom_barri": "la Prosperitat",
      "mode": "public transport",
      "duration_value": 41.3,
      "duration": "41 mins",
      "score": 3.1400261169863306
    },
    {
      "nom_barri": "la Trinitat Nova",
      "mode": "public transport",
      "duration_value": 47.96666666666667,
      "duration": "48 mins",
      "score": 3.171710365911934
    },
    {
      "nom_barri": "Torre Barï",
      "mode": "public transport",
      "duration_value": 56.233333333333334,
      "duration": "56 mins",
      "score": 3.073611111111111
    },
    {
      "nom_barri": "Ciutat Meridiana",
      "mode": "walking",
      "duration_value": 111.5,
      "duration": "1 hour 52 mins",
      "score": 2.4284498452196073
    },
    {
      "nom_barri": "Vallbona",
      "mode": "public transport",
      "duration_value": 52.916666666666664,
      "duration": "53 mins",
      "score": 3.2118055555555554
    },
    {
      "nom_barri": "la Trinitat Vella",
      "mode": "public transport",
      "duration_value": 44.46666666666667,
      "duration": "44 mins",
      "score": 3.055011078789212
    },
    {
      "nom_barri": "Barï de Viver",
      "mode": "public transport",
      "duration_value": 40.55,
      "duration": "41 mins",
      "score": 3.6157452036910773
    },
    {
      "nom_barri": "el Bon Pastor",
      "mode": "public transport",
      "duration_value": 44.95,
      "duration": "45 mins",
      "score": 2.8359323155910063
    },
    {
      "nom_barri": "Sant Andreu",
      "mode": "public transport",
      "duration_value": 37.81666666666667,
      "duration": "38 mins",
      "score": 2.875382871614147
    },
    {
      "nom_barri": "la Sagrera",
      "mode": "public transport",
      "duration_value": 21.6,
      "duration": "22 mins",
      "score": 3.638814901651419
    },
    {
      "nom_barri": "el Congrés i els Indians",
      "mode": "public transport",
      "duration_value": 31.366666666666667,
      "duration": "31 mins",
      "score": 3.147873621387485
    },
    {
      "nom_barri": "Navas",
      "mode": "public transport",
      "duration_value": 34.7,
      "duration": "35 mins",
      "score": 2.790320904838954
    },
    {
      "nom_barri": "el Camp de l'Arpa del Clot",
      "mode": "public transport",
      "duration_value": 28.566666666666666,
      "duration": "29 mins",
      "score": 3.0604993913266476
    },
    {
      "nom_barri": "el Clot",
      "mode": "public transport",
      "duration_value": 18.083333333333332,
      "duration": "18 mins",
      "score": 3.5085271962022158
    },
    {
      "nom_barri": "el Parc i la Llacuna del Poblenou",
      "mode": "public transport",
      "duration_value": 18.45,
      "duration": "18 mins",
      "score": 3.1008107603852046
    },
    {
      "nom_barri": "la Vila Olímpica del Poblenou",
      "mode": "public transport",
      "duration_value": 22.9,
      "duration": "23 mins",
      "score": 1.9625000000000001
    },
    {
      "nom_barri": "el Poblenou",
      "mode": "public transport",
      "duration_value": 16.3,
      "duration": "16 mins",
      "score": 3.0859931682262975
    },
    {
      "nom_barri": "Diagonal Mar i el Front Marítim del Poblenou",
      "mode": "walking",
      "duration_value": 6.433333333333334,
      "duration": "6 mins",
      "score": 2.5
    },
    {
      "nom_barri": "el Besós i el Maresme",
      "mode": "public transport",
      "duration_value": 10.333333333333334,
      "duration": "10 mins",
      "score": 4.135464798992864
    },
    {
      "nom_barri": "Provençals del Poblenou",
      "mode": "public transport",
      "duration_value": 14.416666666666666,
      "duration": "14 mins",
      "score": 3.0297983986083676
    },
    {
      "nom_barri": "Sant Martí de Provençals",
      "mode": "public transport",
      "duration_value": 18.766666666666666,
      "duration": "19 mins",
      "score": 3.574933990958283
    },
    {
      "nom_barri": "la Verneda i la Pau",
      "mode": "public transport",
      "duration_value": 18.066666666666666,
      "duration": "18 mins",
      "score": 3.8781955955622305
    }
  ]
}
```