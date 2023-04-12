import pprint

import boto3
import requests
from jsonschema import validate
import pymysql.cursors

from tests.conftest import get_base_url
from tests.image_schema import valid_schema

url = get_base_url()

connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='mysql_admin',
                             password='password',
                             database='cloudximages',
                             cursorclass=pymysql.cursors.DictCursor)


connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='mysql_admin',
                             password='password',
                             database='cloudximages',
                             cursorclass=pymysql.cursors.DictCursor)


class TestRDSValidation:
    def test_rds_instanse_validation(self):
        response = boto3.client("rds").describe_db_instances()

        assert response['DBInstances'][0]['DBInstanceClass'] == "db.t3.micro"
        assert not response['DBInstances'][0]['MultiAZ']
        assert response['DBInstances'][0]['AllocatedStorage'] == 100
        assert response['DBInstances'][0]['StorageType'] == "gp2"
        assert not response['DBInstances'][0]['StorageEncrypted']
        assert response['DBInstances'][0]['TagList'][3]['Key'] == "cloudx"
        assert response['DBInstances'][0]['Engine'] == "mysql"
        assert response['DBInstances'][0]['EngineVersion'] == "8.0.28"
        assert response['DBInstances'][0]['DBSubnetGroup']['SubnetGroupStatus'] == "Complete"
        assert response['DBInstances'][0]['DBInstanceStatus'] == "available"

    def test_upload_file(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryVA3eImpwyV9Q2EG0",
        }

        data = '------WebKitFormBoundaryVA3eImpwyV9Q2EG0\r\nContent-Disposition: form-data; name="upfile"; ' \
               'filename="app-ui.png"' \
               'Content-Type: ' \
               'image/png\r\n\r\n\r' \
               '------WebKitFormBoundaryVA3eImpwyV9Q2EG0--\r'

        response = requests.post(url=url + "/api/image", headers=headers, data=data, verify=False)

        assert response.status_code == 204

    def test_get_image_metadata(self):
        response = requests.get(url=url + "/api/image/1")

        validate(instance=response.json(), schema=valid_schema)
        assert response.status_code == 200

    def test_delete_image(self):
        response = requests.delete(url=url + "/api/image/1")

        assert response.status_code == 204
        assert response.text == ""

    def test_get_data_from_db(self):
        with connection.cursor() as cursor:
            """
            Result
             {
                'id': 1,
                'last_modified': datetime.datetime(2023, 4, 12, 17, 24, 41),
                'object_key': 'images/bc06f3cc-80ba-4260-8e62-50f3d9395e58-app-ui.png',
                'object_size': 0,
                'object_type': 'binary/octet-stream'
             }
            """
            sql = "SELECT * FROM images"
            cursor.execute(sql)
            result = cursor.fetchone()
            pprint.pprint(result)

