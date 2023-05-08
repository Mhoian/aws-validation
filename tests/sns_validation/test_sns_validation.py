import boto3
import requests

from tests.conftest import get_base_url

url = get_base_url()
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}


class TestSNSValidation:

    def test_sns_validation(self):

        sns_client = boto3.client("sns", region_name='us-east-1')
        response = sns_client.list_topics()
        page = response['Topics'][1]

        response = sns_client.get_topic_attributes(
                TopicArn=page['TopicArn']
            )['Attributes']

        assert "cloudximage-TopicSNSTopic" in response['TopicArn']

    def test_subscribe_email_notification(self):
        email_address = "roman.mhoian777@gmail.com"

        response = requests.post(
            url=url + f"/api/notification/{email_address}",
            headers=headers,
        )

        assert response.status_code == 200

    def tests_get_list_email_subscriptions_to_sns_topic(self):
        response = requests.get(
            url=url + f"/api/notification",
            headers=headers,
        )

        body = response.json()

        assert body[0]["Endpoint"] == "roman.mhoian777@gmail.com"
        assert response.status_code == 200

    def test_delete_subscribed_email_notification(self):
        email_address = "roman.mhoian777@gmail.com"

        response = requests.delete(
            url=url + f"/api/notification/{email_address}",
            headers=headers,
        )

        assert response.status_code == 200