import json
import boto3
from decimal import Decimal

access_key=""
secret_access_key=""
session=boto3.Session(aws_access_key_id='AKIA56RSXOYZPEUFJTR5',aws_secret_access_key='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', region_name='eu-west-1')

client_dynamo=session.resource('dynamodb')
table=client_dynamo.Table('hoods_rent_prices')
records=""

with open('fixed_zeros.json','r') as f:
  records = json.loads(f.read(), parse_float=Decimal)

for i in records:
  response=table.put_item(Item=i)
