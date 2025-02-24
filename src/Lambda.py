import json
import boto3

client = boto3.client("dynamodb")

def lambda_handler(event, context):
    return Get_Visitor_Count()

def Get_Visitor_Count():
    ##
    response = client.scan(TableName="VisitorCountTable")

    ##
    if "Items" in response:
        # Save the response (JSON)
        count = response["Items"][0]["visitor_count"]["N"]
        count = int(count)
    else:
        count = 0
    count += 1

    request = client.update_item(
        ExpressionAttributeNames={
            "#VC": "visitor_count",
        },
        ExpressionAttributeValues={
            ":count": {
                # N is attribute of type number
                "N": str(count),
            },
        },
        Key={
            "visitor_count_id": {
                "N": "1",
            },
        },
        ReturnValues="ALL_NEW",
        TableName="VisitorCountTable",
        # An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them.
        # SET - Adds one or more attributes and values to an item. If any of these attributes already exist, they are replaced by the new values.
        UpdateExpression="SET #VC = :count",
    )

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'visitorcount': count})
    }
