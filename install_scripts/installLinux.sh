#!/bin/bash
set -e

python3 -m venv venv
if [ ! -f "activate" ]; then
	ln -s venv/bin/activate .
fi
. ./activate

pip install --upgrade pip
pip install -i https://hosted.timecoincrypto.net/simple/ miniupnpc==2.1 setproctitle==1.1.10
pip install git+https://github.com/Timecoin-Network/timecoin-blockchain.git@v1.2.0


echo -e "\n===================================================="
echo "Type '. ./activate' to enter the virtual environment"
echo "Type 'deactivate' to leave the virtual environment"
