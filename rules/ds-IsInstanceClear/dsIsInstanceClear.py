# *********************************************************************
# Deep Security - Is Instance Clear?
# *********************************************************************
from __future__ import print_function

# Standard library
import datetime
import json
import urlparse

# Project libraries
import deepsecurity

# 3rd party libraries
import boto3
encryption_capable = False
try:
	from Crypto.Cipher import AES # external dependency
	encryption_capable = True
except Exception, err: pass # we use the flag to ignore


class Decrypter():
	"""
	Utility class to decrypt data using an encrypted data key protected using a KMS master key.
	"""

	def __init__(self, profile_name=None, key=None, context={}, data=""):
		self.key = key
		self.data = data
		self.context = context

		self.session = boto3.session.Session(
			profile_name = profile_name
		)

	def _read(self, data):
		split = urlparse.urlsplit(data)

		if split.scheme == 's3':
			s3 = self.session.resource('s3')
			object = s3.Object(split.netloc, split.path[1:])
			return object.get()['Body'].read()
		elif split.scheme == 'data':
			if ',' in split.path:
				head, payload = split.path.split(',', 1)

				# TODO really we should pay more attention to the header portion
				if 'base64' in head.split(';'):
					return payload.decode('base64')
				else:
					return payload
			else:
				return split.path
# We explicitly do not want file: URI support in our lambda
#		elif split.scheme == 'file':
#			with open(split.path, 'r') as file:
#				return file.read()
		else:
			return data

	def decrypt(self):
		if self.context:
			if not type(self.context) == type({}):
				self.context = json.loads(self._read(self.context))
		else:
			self.context = {}

		key_ciphertext = self._read(self.key)
		client = self.session.client('kms')

		response = client.decrypt(
			CiphertextBlob = key_ciphertext,
			EncryptionContext = self.context
		)

		# http://stackoverflow.com/a/12525165
		unpad = lambda s : s[:-ord(s[len(s)-1:])]

		data = self._read(self.data)

		iv = data[:AES.block_size]
		cipher = AES.new(response['Plaintext'], AES.MODE_CBC, iv)
		plaintext = unpad(cipher.decrypt(data[AES.block_size:]))

		return plaintext

def aws_config_rule_handler(event, context):
	"""
	Primary entry point for the AWS Lambda function

	Verify whether or not the specified instance has any alerts, warnings, or errors

	print() statments are for the benefit of CloudWatch logs & a nod to old school
	debugging ;-)
	"""
	instance_id = None
	is_clear = False
	detailed_msg = ""

	# Make sure the function has been called in the context of AWS Config Rules
	if not event.has_key('invokingEvent') or \
	   not event.has_key('ruleParameters') or \
	   not event.has_key('resultToken') or \
	   not event.has_key('eventLeftScope'):
	   print("Missing a required AWS Config Rules key in the event object. Need [invokingEvent, ruleParameters, resultToken, eventLeftScope]")
	   return { 'result': 'error' }

	# Convert any test events to json (only needed for direct testing through the AWS Lambda Management Console)
	if event.has_key('ruleParameters') and not type(event['ruleParameters']) == type({}): event['ruleParameters'] = json.loads(event['ruleParameters'])
	if event.has_key('invokingEvent') and not type(event['invokingEvent']) == type({}): event['invokingEvent'] = json.loads(event['invokingEvent'])

	# Make sure we have the required rule parameters
	if event.has_key('ruleParameters'):
		if not event['ruleParameters'].has_key('dsUsername') and \
			 not event['ruleParameters'].has_key('dsPassword') and \
			 (not event['ruleParameters'].has_key('dsTenant') and not event['ruleParameters'].has_key('dsHostname')):
			return { 'requirements_not_met': 'Function requires that you at least pass dsUsername, dsPassword, and either dsTenant or dsHostname'}
		else:
			print("Credentials for Deep Security passed to function successfully")

	# Is the function is setup to use encryption but can't import pycrypto, fail gracefully
	if not encryption_capable and event['ruleParameters'].has_key('dsPasswordKey'):
		return  { 'requirements_not_met': "Function is requesting encrypted credntials but can't import pycrypto. Please see https://github.com/deep-security/aws-config/blob/master/README.md#protecting-your-deep-security-manager-api-password for more details" } 

	if encryption_capable:
		# We know that event['ruleParameters']['dsPassword'] exists because of the checks immediately above.
		# Now we need to see if that password needs to be decrypted
		if event['ruleParameters'].has_key('dsPasswordKey'):
			print("Function has password encryption key")
			encryptionContext = event['ruleParameters']['dsPasswordEncryptionContext'] if event['ruleParameters'].has_key('dsPasswordEncryptionContext') else {}
			ds_password = Decrypter(
				key = event['ruleParameters']['dsPasswordKey'],
				context = encryptionContext,
				data = event['ruleParameters']['dsPassword']
			).decrypt()
			print("Function successfully decrypted password")
		else:
			print("Function does not have password encryption key")
			ds_password = event['ruleParameters']['dsPassword']
	else:
		ds_password = event['ruleParameters']['dsPassword']

	# Determine if this is an EC2 instance event
	if event.has_key('invokingEvent'):
	 	if event['invokingEvent'].has_key('configurationItem'):
			if event['invokingEvent']['configurationItem'].has_key('resourceType') and event['invokingEvent']['configurationItem']['resourceType'].lower() == "AWS::EC2::Instance".lower():
				# Something happened to an EC2 instance, we don't worry about what happened
				# the fact that something did is enough to trigger a re-check
				instance_id = event['invokingEvent']['configurationItem']['resourceId'] if event['invokingEvent']['configurationItem'].has_key('resourceId') else None
				if instance_id: print("Target instance [{}]".format(instance_id))
			else:
				print("Event is not targeted towards a resourceType of AWS::EC2::Instance")

	if instance_id:
		# We know this instance ID was somehow impacted, check it's status in Deep Security
		ds_tenant = event['ruleParameters']['dsTenant'] if event['ruleParameters'].has_key('dsTenant') else None
		ds_hostname = event['ruleParameters']['dsHostname'] if event['ruleParameters'].has_key('dsHostname') else None
		ds_port = event['ruleParameters']['dsPort'] if event['ruleParameters'].has_key('dsPort') else 443
		ds_ignore_ssl_validation = bool(event['ruleParameters']['dsIgnoreSslValidation']) if event['ruleParameters'].has_key('dsIgnoreSslValidation') else False
		mgr = None
		try:
			mgr = deepsecurity.dsm.Manager(username=event['ruleParameters']['dsUsername'], password=ds_password, tenant=ds_tenant, hostname=ds_hostname, port=ds_port, ignore_ssl_validation=ds_ignore_ssl_validation)
			mgr.sign_in()
			print("Successfully authenticated to Deep Security")
		except Exception, err:
			print("Could not authenticate to Deep Security. Threw exception: {}".format(err))

		if mgr:
			mgr.computers.get()
			print("Searching {} computers for event source".format(len(mgr.computers)))
			for comp_id, details in mgr.computers.items():
				if details.cloud_object_instance_id and (details.cloud_object_instance_id.lower().strip() == instance_id.lower().strip()):
					print("Found matching computer. Deep Security #{}".format(comp_id))
					detailed_msg = "Current status: {}".format(details.status_light)
					print(detailed_msg)
					if details.status_light.lower() == 'green':
						is_clear = True

			mgr.sign_out() # gracefully clean up our Deep Security session

	# Report the results back to AWS Config
	if detailed_msg:
		result = { 'annotation': detailed_msg }
	else:
		result = {}

	client = boto3.client('config')
	if instance_id:
		compliance = "NON_COMPLIANT"
		if is_clear:
			compliance = 'COMPLIANT'

		try:
			print("Sending results back to AWS Config")
			print('resourceId: {} is {}'.format(event['invokingEvent']['configurationItem']['resourceId'], compliance))

			evaluation = {
				'ComplianceResourceType': event['invokingEvent']['configurationItem']['resourceType'],
				'ComplianceResourceId': event['invokingEvent']['configurationItem']['resourceId'],
				'ComplianceType': compliance,
				'OrderingTimestamp': datetime.datetime.now()
			}

			if detailed_msg:
				evaluation['Annotation'] = detailed_msg

			response = client.put_evaluations(
				Evaluations=[evaluation],
				ResultToken=event['resultToken']
			)

			result['result'] = 'success'
			result['response'] = response
		except Exception, err:
			print("Exception thrown: {}".format(err))
			result['result'] = 'failure'

	print(result)
	return result
