import boto3


class Credentials(object):

    def __init__(self,
                 username_key=None,
                 password_key=None):

        self.username_key = username_key
        self.password_key = password_key

        self.ssm = boto3.client('ssm')

    def get_username(self):
        param_info = self.ssm.get_parameter(
            Name=self.username_key,
            WithDecryption=True
        )
        return param_info['Parameter']['Value']

    def get_password(self):
        param_info = self.ssm.get_parameter(
            Name=self.password_key,
            WithDecryption=True
        )
        return param_info['Parameter']['Value']
