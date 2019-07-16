#!/usr/bin/env bash

set -e

if [ ! -f src/pycrypto-package.zip ]; then
  echo "" >&2
  echo "You need to build the src/pycrypto-package.zip file. To do this, spin up a" >&2
  echo "clean Amazon Linux instance (t2.nano is fine), run build-native.sh there," >&2
  echo "and copy the resulting pycrypto-package.zip file to the src directory." >&2
  echo "" >&2
  echo "Once you've got that done, try this again." >&2
  echo "" >&2
  exit 1
fi

echo ""
echo "Copying dependencies..."

for i in rules/*; do
  unzip -q -o -d $i src/pycrypto-package.zip
  cp -r src/deepsecurity $i
done

echo ""
