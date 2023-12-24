#!/bin/zsh

echo "=================================================NODE START"
sudo curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | zsh
source ~/.zshrc

nvm alias default node
nvm install 'lts/*'

npm install -g yarn


echo "=================================================NODE END"
