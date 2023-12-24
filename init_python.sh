#!/bin/zsh

echo "=================================================ADD PYTHON START"

sudo apt-get upgrade python3
sudo apt install python3-pip

cd ./src
pip3 install -r requirements.txt
cd ..

echo "=================================================ADD PYTHON END"
