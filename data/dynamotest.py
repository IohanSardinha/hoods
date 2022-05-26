import json
import boto3


TABLE_NAME = "hoods_rent_prices"

# Creating the DynamoDB Client
session=boto3.Session(aws_access_key_id='AKIA56RSXOYZPEUFJTR5',aws_secret_access_key='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', region_name='eu-west-1')
client = session.resource('dynamodb')
table = client.Table('hoods_rent_prices')

def lambda_handler(event, context):

    data = table.get_item(
        TableName=TABLE_NAME,
        Key={
            'id': 0
        }
    )
    print(data['Item'])
    
    
lambda_handler(None, None)