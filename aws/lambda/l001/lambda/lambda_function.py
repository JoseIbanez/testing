import logging
import boto3
import json
import decimal
import datetime


#logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(event, context):
    logger.info('got event{}'.format(event))
    message=event['Records'][0]['Sns']['Message']
    dynamo_insert(message)
    return 'OK'

def dynamo_insert(message):

    #Connect to DB
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('temp')

    #Validate message
    logger.info('SNS Message:'+str(message))
    Item=json.loads(message)
    logger.info(Item)

    #Insert message
    response = table.put_item(Item=Item)

    logger.info("PutItem succeeded:")
    logger.info(json.dumps(response, indent=4, cls=DecimalEncoder))

    return 0


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

