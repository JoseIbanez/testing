import json
import boto3
import base64
import re

BUCKET_INC="sl-ibanez-s5p1-incoming"
BUCKET_DEL="sl-ibanez-s5p1-deleted"



def lambda_handler(event, context):
    # TODO implement

    content = parse_event(event)
    if not content:
        return

    filename = scan_mail(content)
    if not filename:
        return

    move_file(filename)


def parse_event(event):

    try:
        print("--event--")
        print(json.dumps(event))
        
        sns_msg = event['Records'][0]['Sns']['Message']
        
        print("--sns--")
        print(sns_msg)
        
        sns = json.loads(sns_msg)
        
        content_b64 = sns['content']
        print("--content b64--")
        print(content_b64)
        
        content = base64.b64decode(content_b64).decode('utf-8')
        print("--content--")
        print(content)
        return content

    except Exception as e:
        print(e)
        return None



def scan_mail(content):

    filename = None
    delete_command = None

    for line in content.split('\n'):

        # Ignore html part
        if "<br>" in line:
            continue


        # Ignore instructions line of original mail
        if "the Delete command" in line:
            continue


        # Detect the "Delete" command
        if "Delete" in line:
            print(line)
            delete_command = True
            continue


        # Detect the filename from original mail
        m = re.search("^filename: (.+)$",line)
        if m:
            filename = m.group(1)
            print(f"{line}, filename: '{filename}'")

        if filename and delete_command:
            break


    if not delete_command:
        return None

    return filename



def move_file(filename):
    s3 = boto3.resource('s3')

    # Copy deleted bucket
    copy_source = {
        'Bucket': BUCKET_INC,
        'Key': filename
    }
    s3.meta.client.copy(copy_source, BUCKET_DEL, filename)

    # Delete from original 
    s3.delete_object(
        Bucket=BUCKET_INC,
        Key=filename)

        