import os
import json
import boto3
from dotenv import load_dotenv

# Environment vairables for auth to AWS
load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
TABLE_NAME = os.getenv("TABLE_NAME")

# Create dynamodb table
client = boto3.client("dynamodb", region_name='us-east-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# The Lambda function handler is the method in your Python code that processes events. When your function is invoked, Lambda runs the handler method.
def lambda_handler(event, context):
    return Get_Visitor_Count()

# Get current count from table, increment count by one, then output the updated count return the updated count JSON for Javascript to read.
def Get_Visitor_Count(TABLE_NAME):

    # Try/Except/Else for Error Handling
    try:
        response = client.scan(TableName=TABLE_NAME)
        # See example_response in /examples dir
        if "Items" in response:
            count = response["Items"][0]["visitor_count"]["N"]
            # Convert string to int for increment operation
            count = int(count)
            # Increment count by 1
            count += 1

    # Error handling for being passed an empty table or non-existent key (sets count to 0, then later creates a new item in the table (update_item()))
    except (IndexError, KeyError):
        count = 0

    # Error handling for being passed a non-existent table (creates a new table with the name of the passed non-existent table)
    except client.exceptions.ResourceNotFoundException:
        client.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'visitor_count_id',
                    'AttributeType': 'N',
                }
            ],
            KeySchema=[
                {
                    'AttributeName': 'visitor_count_id',
                    'KeyType': 'HASH',
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            },
            TableName=TABLE_NAME,
        )
        count = 0

    # Error handling for providing a key element that does not match the schema (ValidationException)
    def get_key_schema():
        # Describe table and get partition key & pk type
        describe_response = client.describe_table(TableName=TABLE_NAME)
        pk_name = describe_response["Table"]["AttributeDefinitions"][0]["AttributeName"]
        pk_type = describe_response["Table"]["AttributeDefinitions"][0]["AttributeType"]

        # Primary key determines pk value
        if pk_type == 'B':
            pk_value = 'MQ=='
            key = {
                f'{pk_name}': {
                    f'{pk_type}': f'{pk_value}',
                }
            }
        elif pk_type == 'S' or pk_type == 'N':
            pk_value = '1'
            key = {
                f'{pk_name}': {
                    f'{pk_type}': f'{pk_value}',
                }
            }

        return key

    client.update_item(
        # Unique identifier of the record.
        Key=get_key_schema(),
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

# Used to execute this script only if the file is ran directly, and not at import.
if __name__ == "__main__":
    Get_Visitor_Count(TABLE_NAME)

