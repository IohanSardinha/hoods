# Database scripts 
All the different scripts that contributed to the creation and upload of the database, divided into three folders and a file
## Data
Contains scripts for managing and cleaning the rent database
## Fetch Maps Data
Contains the scripts to fetch locations data from Google Maps
## Scrape
Contrains the scripts to scrape data from the wikipedia and the news data
## upload.py
A script to add new fields to a DynamoDB used to everytime new data was added to it.
#### Requirements
To use this script, first run:
```bash
$ pip install -r requirements.txt 
```
#### Running
```bash
    $ python upload.py file.json table_name field1|field2
```
- file: Name of the json file, that should be a list of json objects where each of them has an id field
- table_name: The name of the DynamoDB  table
- fields: Name of the fields from the json that will be added to the database with the same name, concatenated by `|`

#### Example
To add a new fields `key1` and `key2` to the table `table`, the `file.json` should be similar to this:
```json
[
    {
        "id": 0,
        "key1": "value1",
        "key2": "value2"
    },
    ...
    {
        "id": 72,
        "key": "value1",
        "key2": "value2"
    },
]
```
And the execution
```bash
    $ python upload.py file.json table key1|key2
```


*All the Scripts that access the database need the access keys to be inserted, so need the file to be edited
