#!/usr/bin/env bash

set -e

source deploy.config

if [[ -z "$LAMBDA_BUCKET" || \
  -z "$LAMBDA_PREFIX" ]]
then
  echo "" >&2
  echo "Required parameters missing in 'deploy.config':" >&2
  echo "  - LAMBDA_BUCKET" >&2
  echo "  - LAMBDA_PREFIX" >&2
  echo "" >&2
  exit 1
fi

./build.sh

echo ""
echo "Packaging Lambda functions..."

sam package \
  --template-file .aws-sam/build/template.yaml \
  --s3-bucket "$LAMBDA_BUCKET" \
  --s3-prefix "$LAMBDA_PREFIX" \
  --output-template-file packaged.yml

echo ""
