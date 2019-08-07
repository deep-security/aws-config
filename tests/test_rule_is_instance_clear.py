from unittest.mock import patch
from src.rules.rule_is_instance_clear import RuleIsInstanceClear


@patch('boto3.client')
@patch('src.rules.rule.Manager')
def test_execute(mock_dsm, mock_client, manager, config_service, event):
    mock_dsm.return_value = manager
    mock_client.return_value = config_service

    rule = RuleIsInstanceClear(event)
    rule.execute()

    assert rule.compliance == 'COMPLIANT'
    assert rule.compliance_msg == 'Current status: GREEN'
