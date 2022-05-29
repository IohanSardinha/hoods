# Fetch Maps Data

## Requirements
To use this script, first run:
```bash
$ pip install -r requirements.txt 
```

## fetchData.py
Script that fetches the locations data from the Google Maps API, for bars, restaurants, dicos, parks, playgrounds and cafés. And save them into the ratings.json file.
#### Usage
```bash
$ python fetchData.py
```

## push_to_db.py
Script that pushes the results of the execution of fetchData.py into the DynamoDB table
#### Usage
```bash
$ python push_to_db.py
```