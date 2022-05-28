import json
import boto3
from decimal import Decimal
import numpy as np
import os

access_key=os.environ['AWS_ACCESS_KEY']
secret_access_key=os.environ['SECRET_AWS_ACCESS_KEY']
session=boto3.Session(aws_access_key_id=access_key,aws_secret_access_key=secret_access_key, region_name='eu-west-1')

client_dynamo=session.resource('dynamodb')
table=client_dynamo.Table('hoods_rent_prices')
with open('ratings.json','r') as f:
  records = json.loads(f.read(), parse_float=Decimal)
  
cats = ["restaurants",
        "cafes",
        "parks",
        "bars",
        "discos",
        "playgrounds"]

for key in records.keys():
    for c in cats:
        if len(records[key][c]) > 0:
            avg_rating = np.array(records[key][c]).sum()/len(records[key][c])
            #if key == 0 and c == "bars": print(len(records[key][c]))
            try:
                item = table.update_item(
                    Key= {
                    "id" : int(key)},
                UpdateExpression= f'SET {c}_num = :input1, {c}_avg = :input2',
                ExpressionAttributeValues={
                        ':input1': Decimal(len(records[key][c])),
                        ':input2' : Decimal(avg_rating)
                    }
                )
            except Exception as e:
                print(e)
     