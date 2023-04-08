from pprint import pprint
from random import choice

import requests
from jsonschema import validate

from tests.s3_validation.image_schema import valid_schema

url = "http://ec2-3-83-137-233.compute-1.amazonaws.com/api/image"


class TestS3Validation:
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

        response = requests.post(url=url, headers=headers, data=data, verify=False)

        assert response.status_code == 204

    def test_download_image_by_id(self):
        image_id = f"/file/1"
        random_num = choice(range(0, 100, 1))

        reposnse = requests.get(url=url + image_id, headers={"Accept": "image/png"}, allow_redirects=True)
        open(f'image_{random_num}.png', 'wb').write(reposnse.content)

        assert reposnse.status_code == 200

    def test_get_all_images(self):
        response = requests.get(url=url)

        assert response.status_code == 200
        pprint(response.json())

    def test_get_image_metadata(self):
        response = requests.get(url=url + "/1")

        validate(instance=response.json(), schema=valid_schema)
        assert response.status_code == 200

    def test_delete_image(self):
        response = requests.delete(url=url + "/1")

        assert response.status_code == 204