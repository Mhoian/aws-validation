import boto3
import pytest
import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


@pytest.fixture(scope="function")
def connect_to_recourse():
    return boto3.resource(
        "ec2",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",
    )


@pytest.fixture(scope="function")
def connect_to_s3_recourse():
    return boto3.resource(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",
    )


def get_base_url():
    response = boto3.client("ec2").describe_instances()
    base_url = "http://" + response["Reservations"][0]["Instances"][0]["PublicDnsName"]

    return base_url
