# KMS encryption / decryption utilities

## Encrypting data
```
usage: encrypt.py [-h] [--profile PROFILE_NAME] [--region REGION_NAME] --keyid
                  KEYID [--context CONTEXT] --data DATA --keyout KEYFILE --out
                  OUTFILE

Encrypt data using a generated data key encrypted with a KMS master key.

optional arguments:
  -h, --help            show this help message and exit
  --profile PROFILE_NAME
                        Use a specific profile from your credential file.
  --region REGION_NAME  The region to use.
  --keyid KEYID         KMS master key ID.
  --context CONTEXT     Encryption context data.
  --data DATA           Plaintext data.
  --keyout KEYFILE      Location to write the encrypted data key.
  --out OUTFILE         Location to write the encrypted data.
```

Example:
```
python encrypt.py \
  --profile profile-name \
  --keyid arn:aws:kms:us-east-1:123456789012:key/... \
  --context file:data.ctx \
  --data file:data.txt \
  --keyout data.key \
  --out data.enc
```

Alternative reading the data from a `data:` URI:
```
python encrypt.py \
  --profile profile-name \
  --keyid arn:aws:kms:us-east-1:123456789012:key/... \
  --context file:data.ctx \
  --data data:text/plain,opensesame \
  --keyout data.key \
  --out data.enc
```

**Warning**: the `data:` URI parsing is pretty basic. If you have any special characters in your input data, either make sure it's base64-encoded on input (example: `data:text/plain;base64,b3BlbiBzZXNhbWU=`) or put it into a file.

# Decrypting data

```
usage: decrypt.py [-h] [--profile PROFILE_NAME] [--region REGION_NAME] --key
                  KEY [--context CONTEXT] --data DATA

Decrypt data encrypted using a KMS data key.

optional arguments:
  -h, --help            show this help message and exit
  --profile PROFILE_NAME
                        Use a specific profile from your credential file.
  --region REGION_NAME  The region to use.
  --key KEY             Encrypted key data.
  --context CONTEXT     Encryption context data.
  --data DATA           Encrypted data.
```

Example:
````
python decrypt.py \
  --profile profile-name \
  --key file:data.key \
  --context file:data.ctx \
  --data file:data.enc
```

Decrypted data is written to standard output. If you want it in a file, use a redirect.

Alternative example, reading objects from Amazon S3:

```
python decrypt.py \
  --profile profile-name \
  --key s3://bucket/path/to/data.key \
  --context s3://bucket/path/to/data.ctx \
  --data s3://bucket/path/to/data.enc
```
