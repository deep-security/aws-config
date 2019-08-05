# *********************************************************************
# Deep Security - Does Instance Have Policy ______?
# *********************************************************************

# Standard library
import logging
logging.getLogger().setLevel(logging.INFO)

from src.rules.rule_does_instance_have_policy import RuleDoesInstanceHavePolicy


def aws_config_rule_handler(event, context):
    try:
        rule = RuleDoesInstanceHavePolicy(event)
        response = rule.execute()
        result = {
            'annotation': rule.compliance_msg,
            'response': response,
            'result': 'success'
        }
    except Exception as ex:
        logging.error('Exception thrown: {}'.format(ex))
        result = {
            'response': ex,
            'result': 'failure'
        }

    return result
