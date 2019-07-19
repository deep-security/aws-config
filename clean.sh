#!/usr/bin/env bash

set -e

echo ""
echo "Cleaning up..."

for i in rules/*; do
  rm -rf $i/Crypto $i/src
done

echo ""
