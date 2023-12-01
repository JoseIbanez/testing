import json
import boto3

COMMON_HEADER = {
    "Access-Control-Allow-Origin" : "*",
    "Access-Control-Allow-Credentials" : True 
}


def lambda_handler(event, context):
    # TODO implement
    print(event)
    
    if not 'body' in event:
        return {
            'statusCode': 500,
            'headers': COMMON_HEADER,
            'body': json.dumps({'Error':'Input body not defined'})
        }

    input = json.loads(event['body'])
        
    if not ('Email' in input or 'Comment' in input or 'Id' in input):
        return {
            'statusCode': 500,
            'headers': COMMON_HEADER,
            'body': json.dumps({'Error':'Missing parameters'})
        }

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Feedback')
    try:
        response = table.put_item(
            Item={
                'Id': input['Id'],
                'Email': input['Email'],
                'Comment': input['Comment']
            })
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': COMMON_HEADER,
            'body': json.dumps({'Error': str(e)})
        }

    return {
        'statusCode': 200,
        'headers': COMMON_HEADER,
        'body': json.dumps('Record has been successfully inserted')
    }
