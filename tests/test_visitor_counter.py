import boto3
from moto import mock_aws
import sys
import os
sys.path.append('/workspaces/M0D_Content/CloudResumeChallenge_Backend/src/')


os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_SECURITY_TOKEN'] = 'testing'
os.environ['AWS_SESSION_TOKEN'] = 'testing'


@mock_aws
def test_empty_table():
    client = boto3.client("dynamodb", region_name='us-east-1')
    table_name = 'test_table'
    from src import visitor_counter_local_v2 as vc
    test_table = client.create_table(
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
    table_name = 'test_table'
    from src import visitor_counter_local_v2 as vc
    vc.Get_Visitor_Count(table_name)
    scan_results = client.scan(TableName=table_name)
    count = scan_results["Items"][0]["visitor_count"]["N"]
    true_false = isinstance(count, str)
    assert true_false == True
