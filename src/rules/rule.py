import logging
import datetime
import distutils.util
import json
import boto3
from src.deepsecurity.credentials import Credentials
from src.deepsecurity.dsm import Manager


class Rule(object):
    def __init__(self, event):
        try:
            self._rule_parameters = json.loads(event['ruleParameters'])
            self._invoking_event = json.loads(event['invokingEvent'])
            self._result_token = event['resultToken']
            self._event_left_scope = event['eventLeftScope']
        except Exception:
            raise ValueError('Missing a required AWS Config Rules key in the event object. \
            Need [invokingEvent, ruleParameters, resultToken, eventLeftScope]')

        self._initialize()

    def _initialize(self):
        self._username_key = self._rule_parameters.get('dsUsernameKey')
        if not self._username_key:
            raise ValueError('Missing parameter: dsUsernameKey')

        self._password_key = self._rule_parameters.get('dsPasswordKey')
        if not self._password_key:
            raise ValueError('Missing parameter: dsPasswordKey')

        self._hostname = self._rule_parameters.get('dsHostname')
        if not self._hostname:
            raise ValueError('Missing parameter: dsHostname')

        self._tenant = self._rule_parameters.get('dsTenant')
        self._port = self._rule_parameters.get('dsPort', 443)
        self._ignore_ssl_validation = distutils.util.strtobool(
            self._rule_parameters.get('dsIgnoreSslValidation', 'False')
        )

        config_item = self._invoking_event.get('configurationItem', {})
        self._resource_type = config_item.get('resourceType')
        if not self._resource_type or self._resource_type != 'AWS::EC2::Instance':
            raise ValueError('Event is not targeted towards a resourceType of AWS::EC2::Instance')
        self._instance_id = config_item.get('resourceId')
        logging.info('Target instance [{}]'.format(self._instance_id))

        self._compliance = 'NON_COMPLIANT'
        self._compliance_msg = 'Details missing'

    @property
    def username_key(self):
        return self._username_key

    @property
    def password_key(self):
        return self._password_key

    @property
    def tenant(self):
        return self._tenant

    @property
    def hostname(self):
        return self._hostname

    @property
    def port(self):
        return self._port

    @property
    def ignore_ssl_validation(self):
        return self._ignore_ssl_validation

    @property
    def instance_id(self):
        return self._instance_id

    @property
    def compliance(self):
        return self._compliance

    @property
    def compliance_msg(self):
        return self._compliance_msg

    def execute(self):
        user_pass = self._get_credentials()
        mgr = Manager(username=user_pass[0], password=user_pass[1], tenant=self._tenant,
                      hostname=self._hostname, port=self._port, ignore_ssl_validation=self._ignore_ssl_validation)
        mgr.sign_in()
        logging.info('Successfully authenticated to Deep Security')

        mgr.computers.get()
        logging.info('Searching {} computers for event source'.format(len(mgr.computers)))

        for comp_id, details in mgr.computers.items():
            if details.cloud_object_instance_id == self._instance_id:
                logging.info('Found matching computer. Deep Security #{}'.format(comp_id))
                self._do_check(details)
                logging.info(self._compliance_msg)

        mgr.sign_out()

        return self._respond_to_config()

    def _get_credentials(self):
        creds = Credentials(self._username_key, self._password_key)
        return creds.get_username(), creds.get_password()

    def _do_check(self, details):
        pass

    def _respond_to_config(self):
        logging.info('Sending results back to AWS Config')
        logging.info('resourceId: {} is {}'.format(self._instance_id, self._compliance))

        evaluation = {
            'ComplianceResourceType': self._resource_type,
            'ComplianceResourceId': self._instance_id,
            'ComplianceType': self._compliance,
            'OrderingTimestamp': datetime.datetime.now(),
            'Annotation': self._compliance_msg
        }

        config_client = boto3.client('config')
        response = config_client.put_evaluations(
            Evaluations=[evaluation],
            ResultToken=self._result_token
        )
        return response
