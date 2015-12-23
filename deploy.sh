#!/bin/sh

set -e

rm -rf deploy
mkdir deploy

if [ -f src/pycrypto-package.zip ]; then
  (cd deploy && unzip -q ../src/pycrypto-package.zip)
else
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
echo "Creating deployment zip files..."

for i in rules/*; do
  rule=`basename $i`
  rm -f deploy/$rule.zip

  (cd src && zip -qr ../deploy/$rule.zip deepsecurity requests suds --exclude __MACOSX .DS_Store *.pyc)
  (cd $i && zip -qr ../../deploy/$rule.zip . --exclude __MACOSX .DS_Store README.md *.pyc)
  (cd deploy && zip -qr $rule.zip Crypto --exclude __MACOSX .DS_Store)

  echo "  deploy/$rule.zip"
done

rm -rf deploy/Crypto

if [ -n "${S3_BASE}" ]; then
  echo ""
  echo "Copying zip files to S3..."

  for i in deploy/ds-*.zip; do
    echo "  \\c"
    aws s3 cp $i $S3_BASE/`basename $i`
  done
fi

echo ""
