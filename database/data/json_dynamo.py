import json
import sys
import boto3
from decimal import Decimal

access_key=""
secret_access_key=""
session=boto3.Session(aws_access_key_id=access_key,aws_secret_access_key=secret_access_key, region_name='eu-west-1')

client_dynamo=session.resource('dynamodb')
table=client_dynamo.Table('___')
records=""

if sys.argc < 2:
    print("usage: python fix_prices.py file.json")

with open(sys.argv[1],'r') as f:
  records = json.loads(f.read(), parse_float=Decimal)

for i in records:
  response=table.put_item(Item=i)
