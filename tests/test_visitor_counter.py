import boto3
from moto import mock_aws
import sys, os


# Set path for src import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Set fake env variables for mocks
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_SECURITY_TOKEN'] = 'testing'
os.environ['AWS_SESSION_TOKEN'] = 'testing'


@mock_aws
def test_empty_table():
    client = boto3.client("dynamodb", region_name='us-east-1')
    table_name = 'empty_table'
    from src import visitor_counter_local_v2 as vc
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
        BillingMode='PAY_PER_REQUEST',
        TableName=table_name,
    )
    vc.Get_Visitor_Count(table_name)
    scan_results = client.scan(TableName=table_name)
    count = scan_results["Items"][0]["visitor_count"]["N"]
    true_false = isinstance(count, str)
    assert true_false == True


@mock_aws
def test_table_does_not_exist():
    client = boto3.client("dynamodb", region_name='us-east-1')
    table_name = 'non_existent_table'
    from src import visitor_counter_local_v2 as vc
    vc.Get_Visitor_Count(table_name)
    scan_results = client.scan(TableName=table_name)
    count = scan_results["Items"][0]["visitor_count"]["N"]
    true_false = isinstance(count, str)
    assert true_false == True


@mock_aws
def test_schema_validation_error():
    client = boto3.client("dynamodb", region_name='us-east-1')
    table_name = 'invalid_schema_table'
    from src import visitor_counter_local_v2 as vc
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'visitor_count_id',
                'AttributeType': 'B',
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'visitor_count_id',
                'KeyType': 'HASH',
            }
        ],
        BillingMode='PAY_PER_REQUEST',
        TableName=table_name,
    )
    vc.Get_Visitor_Count(table_name)
    scan_results = client.scan(TableName=table_name)
    count = scan_results["Items"][0]["visitor_count"]["N"]
    true_false = isinstance(count, str)
    assert true_false == True
