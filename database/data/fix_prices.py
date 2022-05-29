import json
import sys
import boto3
from decimal import Decimal

TABLE_NAME = "_______"

# Creating the DynamoDB Client
session=boto3.Session(aws_access_key_id='______',aws_secret_access_key='________/6N5pwMq', region_name='eu-west-1')
client = session.resource('dynamodb')
table = client.Table(TABLE_NAME)

if sys.argc < 2:
    print("usage: python fix_prices.py file.json")

with open(sys.argv[1],'r') as f:
  records = json.loads(f.read(), parse_float=Decimal)

for record in records:
    
    preu = {"y"+k:v for k,v in record["Preu"].items()}
    preuM2 = {"y"+k:v for k,v in record["PreuM2"].items()}
    
    table.update_item(
            Key= {
            "id" : int(record["id"])},
            UpdateExpression= 'SET Preu = :input1, PreuM2 = :input2',
            ExpressionAttributeValues={
                ':input1': preu,
                ':input1': preuM2
            }
        )
    
