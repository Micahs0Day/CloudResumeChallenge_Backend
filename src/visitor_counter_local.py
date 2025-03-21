import os
import json
import boto3
from dotenv import load_dotenv

# Environment variables for auth to AWS
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
TABLE_NAME = os.getenv("TABLE_NAME")

client = boto3.client("dynamodb", region_name='us-east-1',
                      aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# The Lambda function handler is the method in your Python code that processes events. When your function is invoked, Lambda runs the handler method.
def lambda_handler(event, context):
    return Get_Visitor_Count()

# Get current count from table, increment count by one, then output the updated count return the updated count JSON for Javascript to read.
def Get_Visitor_Count(table):

    # The Scan operation returns one or more items and item attributes by accessing every item in a table or a secondary index.
    # You can also use the you can provide a FilterExpression operation to limit results.
    response = client.scan(TableName=table)
    
    # See example_response in /examples dir
    if "Items" in response:
        count = response["Items"][0]["visitor_count"]["N"]
        # Convert string to int for increment operation
        count = int(count)
        # Increment count by 1
        count += 1

    # An attribute is a data element that describes a particular item in a table!

    # update_item() = Edits an existing item’s attributes, or adds a new item to the table if it does not already exist.
    request = client.update_item(
        # Unique identifier of the record.
        Key={
            "visitor_count_id": {
                "N": "1",
            },
        },
        # Substitution token for attribute name.
        ExpressionAttributeNames={
            "#VC": "visitor_count",
        },
        # One or more values that can be substituted in an expression.
        # Use the : (colon) character in an expression to dereference an attribute value.
        # Dereferencing allows us to access the value stored at the memory address pointed to by that pointer (reference).
        ExpressionAttributeValues={
            ":count": {
                # N (string) is attribute of type number
                "N": str(count),
            },
        },
        # ALL_NEW = Returns all of the attributes of the item, as they appear after the UpdateItem operation.
        ReturnValues="ALL_NEW",
        TableName=TABLE_NAME,
        # An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them.
        # SET - Adds one or more attributes and values to an item. If any of these attributes already exist, they are replaced by the new values.
        UpdateExpression="SET #VC = :count",
    )
    # JSON response for updated count (will be read by our frontend JS code)
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'visitorcount': count})
    }


print(Get_Visitor_Count(TABLE_NAME))
