import json
import boto3
from botocore.exceptions import ClientError

SENDER = "File processor bot <bot@com.com.es>"
RECIPIENT = "jose.ibanez@vodafone.com"
AWS_REGION = "us-east-1"
CHARSET = "UTF-8"



def lambda_handler(event, context):
    print(json.dumps(event))
    
    body=json.loads(event['Records'][0]['body'])
    send_mail(body)




def send_mail(body):

    try:
        filename = body['Records'][0]['s3']['object']['key']
        size =     body['Records'][0]['s3']['object']['size']
        eTag =     body['Records'][0]['s3']['object']['eTag']
        dateTime = body['Records'][0]['eventTime']
    except:
        print("Bad body")
        print(body)
        return


    SUBJECT = "New file uploaded"

    BODY_TEXT = ("Amazon SES Email new file uploaed\r\n"
                "\r\n"
                f"filename: {filename}\r\n"
                f"date: {dateTime}\r\n"
                f"size: {size}\r\n"
                f"eTag: {eTag}\r\n"
                "\r\n"
                "If you want to remove this file answer this mail with the Delete command.\r\n"
                "\r\n"
                "Regards\r\n"
                )


    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Source=SENDER,
            Destination={ 'ToAddresses': [ RECIPIENT ] },
            Message={
                'Subject': { 'Charset': CHARSET, 'Data': SUBJECT },
                'Body': {
                    'Text': { 'Charset': CHARSET, 'Data': BODY_TEXT },
                }
            }
        )


    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

