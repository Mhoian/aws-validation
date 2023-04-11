from pprint import pprint

import requests
import pytest
from tests.conftest import get_base_url

url = get_base_url()


class TestAwsInstanceValidation:
    @pytest.mark.parametrize(
        "instance_type,instance_tag,device_size,instance_os,public_ip",
        [
            (
                "t2.micro",
                "cloudx",
                8,
                "Linux/UNIX",
                "44.204.152.65",
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
        instance = connect_to_recourse.Instance("i-031ba3fca2133380a")

        assert instance.instance_type == instance_type
        assert instance.tags[2]["Key"] == instance_tag
        assert (
            instance.image.block_device_mappings[0]["Ebs"]["VolumeSize"] == device_size
        )
        assert instance.platform_details == instance_os
        assert instance.public_ip_address == public_ip

    @pytest.mark.parametrize(
        "instance_type,instance_tag,device_size,instance_os,private_ip",
        [("t2.micro", "cloudx", 8, "Linux/UNIX", "10.0.81.88")],
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
        instance = connect_to_recourse.Instance("i-0ce7996073c610eec")

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
    def test_get_application_information(
        self, aws_region, availability_zone, private_ip_address
    ):
        response = requests.get(url=url, headers={"accept": "application/json"}).json()
        print(response)

        assert response["region"] == aws_region
        assert response["availability_zone"] == availability_zone
        assert response["private_ipv4"] == private_ip_address

    @pytest.mark.parametrize(
        "cidr_block,vpc_tags",
        [("10.0.0.0/16", "cloudx")],
    )
    def test_vpc_validation(self, connect_to_recourse, cidr_block, vpc_tags):
        instance = connect_to_recourse.Instance("i-031ba3fca2133380a")

        assert instance.network_interfaces[0].vpc.cidr_block == cidr_block
        assert instance.vpc.tags[4]['Key'] == vpc_tags

    def test_s3_validation(self, connect_to_s3_recourse):
        response = connect_to_s3_recourse.Bucket(
            "cloudximage-imagestorebucketf57d958e-n28kaktvf5a"
            )

        pprint(response)


