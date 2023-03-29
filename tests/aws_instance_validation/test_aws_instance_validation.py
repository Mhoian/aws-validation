import requests
import pytest

url = "http://ec2-18-205-115-43.compute-1.amazonaws.com"


class TestAwsInstanceValidation:
    @pytest.mark.parametrize(
        "instance_type,instance_tag,device_size,instance_os,public_ip",
        [
            (
                    "t2.micro",
                    "cloudx",
                    8,
                    "Linux/UNIX",
                    "18.205.115.43",
            )
        ],
    )
    def test_get_public_instance_information(
            self,
            connect_to_recourse,
            instance_type,
            instance_tag,
            device_size,
            instance_os,
            public_ip,
    ):
        instance = connect_to_recourse.Instance("i-0b77f8d03c21685f1")

        assert instance.instance_type == instance_type
        assert instance.tags[1]["Key"] == instance_tag
        assert (
                instance.image.block_device_mappings[0]["Ebs"]["VolumeSize"] == device_size
        )
        assert instance.platform_details == instance_os
        assert instance.public_ip_address == public_ip

    @pytest.mark.parametrize(
        "instance_type,instance_tag,device_size,instance_os,private_ip",
        [("t2.micro", "cloudx", 8, "Linux/UNIX", "10.0.142.24")],
    )
    def test_get_private_instance_information(
            self,
            connect_to_recourse,
            instance_type,
            instance_tag,
            device_size,
            instance_os,
            private_ip,
    ):
        instance = connect_to_recourse.Instance("i-069e49695f8c29018")

        assert instance.instance_type == instance_type
        assert instance.tags[1]["Key"] == instance_tag
        assert (
                instance.image.block_device_mappings[0]["Ebs"]["VolumeSize"] == device_size
        )
        assert instance.platform_details == instance_os
        assert instance.private_ip_address == private_ip
        assert not instance.public_ip_address

    @pytest.mark.parametrize(
        "aws_region,availability_zone,private_ip_address",
        [("us-east-1", "us-east-1a", "10.0.118.18")],
    )
    def test_get_application_information(self, aws_region, availability_zone, private_ip_address):
        response = requests.get(url=url, headers={"accept": "application/json"}).json()
        print(response)

        assert response["region"] == aws_region
        assert response["availability_zone"] == availability_zone
        assert response["private_ipv4"] == private_ip_address
