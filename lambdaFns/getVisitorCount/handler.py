import json
import os
import boto3

ddb = boto3.client("dynamodb")
table = os.environ["TABLE_NAME"]

def handler(event, context):
    params = {
        'TableName': f"{table}",
        'Key': {
            'id': {
                'S': 'visitors'
            }
        },
        'UpdateExpression': 'ADD visitor_count :incr',
        'ExpressionAttributeValues': {
            ':incr': {
                'N': '1'
            }
        },
        'ReturnValues': 'UPDATED_NEW'
    }

    # Update the item in the table
    result = ddb.update_item(**params)

    
    item = result['Attributes']['visitor_count']['N']

    # Return the updated item
    return {"headers": {"Content-Type" : "application/json"}, "statusCode": 200, "body": item}
   
