#!/usr/bin/env bash

set -e

source deploy.config

if [[ -z "$STACK_NAME" || \
  -z "$CONFIG_BUCKET" || \
  -z "$CONFIG_PREFIX" || \
  -z "$DS_USERNAME_PARAM_STORE_KEY" || \
  -z "$DS_PASSWORD_PARAM_STORE_KEY" || \
  -z "$DS_HOSTNAME" || \
  -z "$DS_POLICY" || \
  -z "$DS_CONTROL" ]]
then
  echo "" >&2
  echo "Required parameters missing in 'deploy.config':" >&2
  echo "  - STACK_NAME" >&2
  echo "  - CONFIG_BUCKET" >&2
  echo "  - CONFIG_PREFIX" >&2
  echo "  - DS_USERNAME_PARAM_STORE_KEY" >&2
  echo "  - DS_PASSWORD_PARAM_STORE_KEY" >&2
  echo "  - DS_HOSTNAME" >&2
  echo "  - DS_POLICY" >&2
  echo "  - DS_CONTROL" >&2
  echo "" >&2
  exit 1
fi

./package.sh

echo ""
echo "Deploying Lambda functions and Config rules..."

sam deploy \
  --stack-name "$STACK_NAME" \
  --template-file packaged.yml \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    ConfigBucket="$CONFIG_BUCKET" \
    ConfigPrefix="$CONFIG_PREFIX" \
    DSUsernameKey="$DS_USERNAME_PARAM_STORE_KEY" \
    DSPasswordKey="$DS_PASSWORD_PARAM_STORE_KEY" \
    DSHostname="$DS_HOSTNAME" \
    DSPort="$DS_PORT" \
    DSTenant="$DS_TENANT" \
    DSIgnoreSslValidation="$DS_IGNORE_SSL_VALIDATION" \
    DSPolicy="$DS_POLICY" \
    DSControl="$DS_CONTROL"

./clean.sh

echo ""
