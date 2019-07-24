#!/usr/bin/env bash

set -e

echo ""
echo "Running unit tests..."

pytest -s -vv tests/unit

echo ""
echo "Copying dependencies..."

for i in rules/*; do
  cp -r src tests requirements.txt $i
done

echo ""
echo "Building from source..."

if [[ "`uname`" == "Linux" ]]; then
  sam build -t deep-security.yml
else
  sam build -t deep-security.yml -u
fi

echo ""
