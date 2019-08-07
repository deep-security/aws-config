from unittest.mock import patch, MagicMock
from src.rules.rule import Rule


def test_requirement(event):
    rule = Rule(event)
    assert rule.username_key
    assert rule.password_key
    assert rule.hostname


@patch('src.deepsecurity.credentials.Credentials.get_password')
@patch('src.deepsecurity.credentials.Credentials.get_username')
def test_get_credentials(mock_get_username, mock_get_password, event):
    mock_get_username.return_value = 'user'
    mock_get_password.return_value = 'pass'

    rule = Rule(event)
    creds = rule._get_credentials()
    assert creds == ('user', 'pass')


@patch('boto3.client')
def test_respond_to_config(mock_client, config_response, event):
    config = MagicMock()
    config.put_evaluations.return_value = config_response
    mock_client.return_value = config

    rule = Rule(event)
    response = rule._respond_to_config()
    assert response == config_response
