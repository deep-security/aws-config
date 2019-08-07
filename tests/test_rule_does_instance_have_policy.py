from unittest.mock import patch
from src.rules.rule_does_instance_have_policy import RuleDoesInstanceHavePolicy


def test_requirement(event_policy):
    rule = RuleDoesInstanceHavePolicy(event_policy)
    assert rule.username_key
    assert rule.password_key
    assert rule.hostname
    assert rule.policy


@patch('boto3.client')
@patch('src.rules.rule.Manager')
def test_execute(mock_dsm, mock_client, manager, config_service, event_policy):
    mock_dsm.return_value = manager
    mock_client.return_value = config_service

    rule = RuleDoesInstanceHavePolicy(event_policy)
    rule.execute()

    assert rule.compliance == 'COMPLIANT'
    assert rule.compliance_msg == 'Current policy: Linux Server'
