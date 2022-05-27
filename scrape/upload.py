import json
import boto3
from decimal import Decimal

TABLE_NAME = "hoods_rent_prices"

# Creating the DynamoDB Client
session=boto3.Session(aws_access_key_id='AKIA56RSXOYZPEUFJTR5',aws_secret_access_key='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', region_name='eu-west-1')
client = session.resource('dynamodb')
table = client.Table('hoods_rent_prices')

with open('imgs.json','r') as f:
  records = json.loads(f.read(), parse_float=Decimal)

for record in records:
  
    table.update_item(
            Key= {
            "id" : int(record["id"])},
            UpdateExpression= 'SET img = :input1',
            ExpressionAttributeValues={
                #':input1': record['center']
                ':input1': record['img']
            }
        )
    
