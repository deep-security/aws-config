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

	description = """Decrypt data encrypted using a KMS data key."""

	parser = argparse.ArgumentParser(description=description)

	parser.add_argument('--profile', action='store', dest='profile_name', required=False, help='Use a specific profile from your credential file.')
	parser.add_argument('--region', action='store', dest='region_name', required=False, help='The region to use.')

	parser.add_argument('--key', action='store', dest='key', required=True, help='Encrypted key data.')
	parser.add_argument('--context', action='store', dest='context', required=False, help='Encryption context data.')
	parser.add_argument('--data', action='store', dest='data', required=True, help='Encrypted data.')

	if str_to_parse:
		return parser.parse_args(str_to_parse)
	else:
		return parser.parse_args()

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
		elif split.scheme == 'file':
			with open(split.path, 'r') as file:
				return file.read()
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

class ScriptContext():
	"""
	"""

	def __init__(self, args):
		self.args = args

	def decrypt(self):
		plaintext = Decrypter(
			profile_name = self.args.profile_name,
			key = self.args.key,
			context = self.args.context,
			data = self.args.data
		).decrypt()

		print(plaintext)

def main():
	context = ScriptContext(parse_args())
	context.decrypt()

if __name__ == '__main__': main()
