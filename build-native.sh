#!/bin/sh

# Run this on a clean Amazon Linux instance to create the pycrypto-package.zip file.
# Then copy the pycrypto-package.zip file to the repository.

set -ex

# http://markn.ca/2015/10/python-extension-modules-in-aws-lambda/
sudo yum -y update
sudo yum -y groupinstall "Development Tools"
sudo yum -y install Cython --enablerepo=epel

rm -rf aws-config

virtualenv aws-config

cd aws-config

source bin/activate

pip install --upgrade pip

pip install --no-cache-dir pycrypto

# Hack around us not knowing whether to expect in dist-packages or site-packages
cd lib64/python2.7/*-packages/Crypto/..

rm -f "${HOME}/pycrypto-package.zip"

zip -qr "${HOME}/pycrypto-package.zip" Crypto

echo "Built ${HOME}/pycrypto-package.zip"
