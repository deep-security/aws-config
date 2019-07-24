#!/usr/bin/env bash

set -e

echo ""
echo "Cleaning up..."

for i in rules/*; do
  rm -rf $i/src $i/tests $i/requirements.txt
done

rm -rf .aws-sam

echo ""
