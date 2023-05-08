import boto3
import requests

from tests.conftest import get_base_url

url = get_base_url()


class TestServerlessValidation:
    def test_dynamodb_instanse_validation(self):
        client = boto3.client("dynamodb")
        list_tables = client.list_tables()
        table_name = list_tables["TableNames"][0]
        table_reqs = client.describe_table(TableName=table_name)
        time_to_live = client.describe_time_to_live(TableName=table_name)

        assert "cloudxserverless-DatabaseImagesTable" in table_reqs["Table"]["TableName"]
        assert table_reqs['Table']['ProvisionedThroughput']['ReadCapacityUnits'] == 5
        assert table_reqs['Table']['ProvisionedThroughput']['WriteCapacityUnits'] == 1
        assert time_to_live['TimeToLiveDescription']['TimeToLiveStatus'] == 'DISABLED'

    def test_aws_lambda_validation(self):
        client = boto3.client("lambda")
        list_functions = client.list_functions()
        event_hendler_reqs = list_functions['Functions'][3]

        assert event_hendler_reqs['Timeout'] == 3
        assert event_hendler_reqs['MemorySize'] == 128
        assert event_hendler_reqs['EphemeralStorage']['Size'] == 512

    def test_upload_file(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryVA3eImpwyV9Q2EG0",
        }

        data = (
            '------WebKitFormBoundaryVA3eImpwyV9Q2EG0\r\nContent-Disposition: form-data; name="upfile"; '
            'filename="app-ui.png"'
            "Content-Type: "
            "image/jpg\r\n\r\n\r"
            "------WebKitFormBoundaryVA3eImpwyV9Q2EG0--\r"
        )

        response = requests.post(
            url=url + "/api/image", headers=headers, data=data, verify=False
        )

        assert response.status_code == 200