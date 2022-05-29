import json
import boto3
from decimal import Decimal
import sys


if sys.argc < 3:
  print("usage: python upload.py table_name field1|field2...")

TABLE_NAME = sys.argv[1]

# Creating the DynamoDB Client
session=boto3.Session(aws_access_key_id='__________',aws_secret_access_key='___________', region_name='eu-west-1')
client = session.resource('dynamodb')
table = client.Table(TABLE_NAME)

with open('imgs.json','r') as f:
  records = json.loads(f.read(), parse_float=Decimal)

for record in records:
  
    table.update_item(
            Key= {
            "id" : int(record["id"])},
            UpdateExpression= "SET "+ ",".join(v+" = "+":input"+str(i) for i,v in enumerate(sys.argv[2].split("|"))),
            ExpressionAttributeValues={":input"+str(i):records[v] for i,v in  enumerate(sys.argv[2].split("|"))}
        )
    
