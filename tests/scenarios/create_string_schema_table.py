import os
import boto3
from dotenv import load_dotenv

# Environment variables for auth to AWS
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
TABLE_NAME = "test_string_schema_table"

client = boto3.client("dynamodb", region_name='us-east-1',
                      aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def create_string_schema_table():
    request = client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'visitor_count_id',
                'AttributeType': 'S',
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'visitor_count_id',
                'KeyType': 'HASH',
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        TableName=TABLE_NAME,
    )
    print(request)

def get_key_schema2():
    # Describe table and get partition key & pk type
    describe_response = client.describe_table(TableName=TABLE_NAME)
    pk_type = describe_response["Table"]["AttributeDefinitions"][0]["AttributeType"]
    return pk_type

create_string_schema_table()
 
#print(get_key_schema2())
