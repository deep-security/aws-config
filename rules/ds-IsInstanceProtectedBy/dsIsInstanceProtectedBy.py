# *********************************************************************
# Deep Security - Is Instance Protected By _______?
# *********************************************************************

# Standard library
import logging
logging.getLogger().setLevel(logging.INFO)

from src.rules.rule_is_instance_protected_by import RuleIsInstanceProtectedBy


def aws_config_rule_handler(event, context):
    try:
        rule = RuleIsInstanceProtectedBy(event)
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
