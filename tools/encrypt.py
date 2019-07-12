import argparse
import urlparse
import json

import boto3

from Crypto.Cipher import AES
from Crypto import Random

def parse_args(str_to_parse=None):
	"""
	Parse command-line arguments
	"""

	description = """Encrypt data using a generated data key encrypted with a KMS master key."""

	parser = argparse.ArgumentParser(description=description)

	parser.add_argument('--profile', action='store', dest='profile_name', required=False, help='Use a specific profile from your credential file.')
	parser.add_argument('--region', action='store', dest='region_name', required=False, help='The region to use.')

	parser.add_argument('--keyid', action='store', dest='keyid', required=True, help='KMS master key ID.')
	parser.add_argument('--context', action='store', dest='context', required=False, help='Encryption context data.')
	parser.add_argument('--data', action='store', dest='data', required=True, help='Plaintext data.')
	parser.add_argument('--keyout', action='store', dest='keyfile', required=True, help='Location to write the encrypted data key.')
	parser.add_argument('--out', action='store', dest='outfile', required=True, help='Location to write the encrypted data.')

	if str_to_parse:
		return parser.parse_args(str_to_parse)
	else:
		return parser.parse_args()

class ScriptContext():
	"""
	"""

	def __init__(self, args):
		self.args = args
		self.session = boto3.session.Session(
			region_name=args.region_name,
			profile_name=args.profile_name
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
		elif split.scheme == 'file':
			with open(split.path, 'r') as file:
				return file.read()
		else:
			return data

	def encrypt(self):
		if self.args.context:
			context = json.loads(self._read(self.args.context))
		else:
			context = {}

		client = self.session.client('kms')

		response = client.generate_data_key(
				KeyId=self.args.keyid,
				EncryptionContext=context,
				KeySpec='AES_256'
		)

		with open(self.args.keyfile, 'w') as datakey_ciphertext_file:
			datakey_ciphertext_file.write(response['CiphertextBlob'])

		iv = Random.new().read(AES.block_size)
		cipher = AES.new(response['Plaintext'], AES.MODE_CBC, iv)

		# http://stackoverflow.com/a/12525165
		BS = AES.block_size
		pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

		padded = pad(self._read(self.args.data))

		with open(self.args.outfile, 'w') as data_file:
			data_file.write(iv)
			data_file.write(cipher.encrypt(padded))

		print("Generated data key in: " + self.args.keyfile)
		print("Encrypted data in: " + self.args.outfile)

		if self.args.context:
			print("Encryption context in: " + self.args.context)

def main():
	context = ScriptContext(parse_args())
	context.encrypt()

if __name__ == '__main__': main()
