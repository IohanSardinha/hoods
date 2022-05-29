import simplejson
from datetime import datetime
import requests
import boto3
from boto3.dynamodb.conditions import Key

SCORES_TABLE_NAME = "hoods_rent_prices"
NEWS_TABLE_NAME = "scraped_news"

# Creating the DynamoDB Client
dynamodb_client = boto3.client('dynamodb', region_name="eu-west-1")

# Creating the DynamoDB Table Resource
dynamodb = boto3.resource('dynamodb', region_name="eu-west-1")
scores_table = dynamodb.Table(SCORES_TABLE_NAME)
news_table = dynamodb.Table(NEWS_TABLE_NAME)

def lambda_handler(event, context):
    
    operation = event['httpMethod']
    if operation == 'GET':
        if int(event['queryStringParameters']['id']) < 0 or int(event['queryStringParameters']['id']) > 72:
            return {
                'statusCode': 400,
                'body': 'Index out of bounds'
                
            }
    
        if not 'id' in event['queryStringParameters']:
            return {
                'statusCode': 400,
                'body': 'Missing id'
                
            }
    
        
        try:
            response = scores_table.get_item(
                TableName=SCORES_TABLE_NAME,
                Key={
                    'id': int(event['queryStringParameters']['id'])
                }
            )
            
            news = scores_table.get_item(
                TableName=NEWS_TABLE_NAME,
                Key={
                    'id': int(response["Item"]["Codi_Districte"])
                }
            )
            
            # print(news)
            
            response["Item"]["news"] = news["Item"]["news"]
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET'
                },
                'body': simplejson.dumps(response['Item'])
            }
            
        except Exception as ex:
            return {
                'statusCode': 500,
                'body': str(ex)
            }
            
    else:
        return {
        'statusCode': '400',
        'body': json.dumps(str(ValueError('Unsupported method %s'%operation)))
    }

        
        
        
    
    
