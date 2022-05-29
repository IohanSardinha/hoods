# Scrape
Scripts to scrape data from the wikipedia and the news data

## scrape_descriptions.py
Scrape the descriptions of all Barcelona barrios from wikipedia in english, the data needs to be uploaded from output.json using upload.py from the database folder.
#### Usage
```bash
$ python scrape_descriptions.py >> output.json
```

## scrape_descriptions.py
Scrape the images of all Barcelona barrios from catalan wikipedia(The english version does not have images for all barrios), the data needs to be uploaded from output.json using upload.py from the database folder.

#### Usage
```bash
$ python scrape_images.py >> output.json
```

## scrape_news.py
Scrape the news from the Barcelona Ajuntamento site, for each district and adds them to the table
#### Usage
```bash
$ python scrape_news.py
```