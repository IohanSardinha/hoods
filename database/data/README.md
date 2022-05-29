# Data
Scripts for managing and cleaning the rent database 
## Requirements
To use this scripts, first run:
```bash
$ pip install -r requirements.txt
```


## preprocessing.ipynb
A jupyter notebook with that preprocesses the data from the rent csv's, through a series of aggregations and operations, into a json to be uploaded to the DynamoDB

## change_data.py
A script that changes the format of the json produced by the preprocessing.ipynb. In the original json the barrios are separated by year, this agregates them by id having the prices as a dictionary of key= year, value= price for year.
#### Usage
```bash
$ python change_data.py input.json output.json
```

## fix_zeros.py
A script that takes the output json from change_data.py that has the missing prices as 0 and change them to the year of the price of the closest year.
#### Usage
```bash
$ python fix_zeros.py input.json output.json
```

## json_dynamo.py
A script that uploads the a json file to a table in DynamoDB, the name of the table must be changed in the file. It's different from the upload.py script in the database folder because it's the first upload, to a blank database. The upload.py updates or adds new fields to an already populated table.
#### Usage
```bash
$ python json_dynamo.py file.json
```

### get_center.py
A script to compute the centroids of the polygons
#### Usage
```bash
$ python get_center.py file.json output.json
```

## fix_prices.py
A script that adds a `y` in front of the key for the years in the table, since it was causing trouble in the frontend 
#### Usage
```bash
$ python fix_prices.py file.json
```