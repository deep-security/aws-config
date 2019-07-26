#!/usr/bin/env bash

set -e

./package.sh

echo ""
echo "Publishing to AWS Serverless Application Repository..."

sam publish --template packaged.yml

./clean.sh

echo ""
