import datetime
from unittest.mock import patch, MagicMock
from src.deepsecurity.credentials import Credentials


@patch('boto3.client')
def test_get_username(mock_client):
    ssm = MagicMock()
    ssm.get_parameter.return_value = {
        'Parameter': {
            'ARN': u'arn:aws:ssm:us-west-1:000000000000:parameter/ds/api_user',
            'LastModifiedDate': datetime.datetime(2019, 7, 23, 15, 43, 26, 375000),
            'Name': u'/ds/api_user',
            'Type': u'SecureString',
            'Value': u'admin',
            'Version': 1
        }
    }
    mock_client.return_value = ssm

    credentials = Credentials('/ds/api_user', '/ds/api_password')
    username = credentials.get_username()

    assert username == 'admin'


@patch('boto3.client')
def test_get_password(mock_client):
    ssm = MagicMock()
    ssm.get_parameter.return_value = {
        'Parameter': {
            'ARN': u'arn:aws:ssm:us-west-1:000000000000:parameter/ds/api_password',
            'LastModifiedDate': datetime.datetime(2019, 7, 23, 15, 43, 26, 375000),
            'Name': u'/ds/api_password',
            'Type': u'SecureString',
            'Value': u'password',
            'Version': 1
        }
    }
    mock_client.return_value = ssm

    credentials = Credentials('/ds/api_user', '/ds/api_password')
    password = credentials.get_password()

    assert password == 'password'
