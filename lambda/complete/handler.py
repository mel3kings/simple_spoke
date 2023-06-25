import json, urllib, boto3, csv

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
retroTable = dynamodb.Table('mel3kings-prod-subscribedusers');


def lambda_handler(event, context):
    print("Event received by Lambda function: " + json.dumps(event, indent=2))
    print(event)
    try:
        retroTable.put_item(Item=event)
    except Exception as e:
        print("============!!!ERROR!!!=======")
        print(e)
        errorResponse = {
            "statusCode": 404,
            "headers": {},
            "body": e,
            "isBase64Encoded": "false"
        }
        return errorResponse
    response = {
        "statusCode": 200,
        "headers": {},
        "body": "Success",
        "isBase64Encoded": "false"
    }
    return response
