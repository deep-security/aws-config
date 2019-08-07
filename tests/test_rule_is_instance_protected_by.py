from unittest.mock import patch
from src.rules.rule_is_instance_protected_by import RuleIsInstanceProtectedBy


def test_requirement(event_control):
    rule = RuleIsInstanceProtectedBy(event_control)
    assert rule.username_key
    assert rule.password_key
    assert rule.hostname
    assert rule.control


@patch('boto3.client')
@patch('src.rules.rule.Manager')
def test_execute(mock_dsm, mock_client, manager, config_service, event_control):
    mock_dsm.return_value = manager
    mock_client.return_value = config_service

    rule = RuleIsInstanceProtectedBy(event_control)
    rule.execute()

    assert rule.compliance == 'COMPLIANT'
    assert rule.compliance_msg == 'Firewall status: Firewall: On, 8 rules'
