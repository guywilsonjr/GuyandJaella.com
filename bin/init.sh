#!/usr/bin/env bash
export REPO_NAME='GuyandJaella.com'
# To install run chmod +x env/{REPO_NAME}bin/init.sh && yes | ENV/{REPO_NAME}/init.sh
rm ~/environments/README.md
# Update and install python3.7. Write over python3.6 because alternatives don't like to recognize python3.7 installed from source

sudo yum -y update
sudo yum -y upgrade
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
sudo tar xzf Python-3.7.3.tgz
sudo rm Python-3.7.3.tgz
cd Python-3.7.3
sudo ./configure --enable-optimizations --prefix /usr
sudo make altinstall
cd ~/environment/
sudo rm -rf /usr/src/Python-3.7.3
sudo rm /usr/bin/python3.6
# Comment to not re-write python 3.7 to backup
# sudo cp /usr/bin/python3.6 /usr/bin/python3.6.backup
sudo cp /usr/bin/python3.7 /usr/bin/python3.6
sudo alternatives --set python /usr/bin/python3.6
python3 -m venv env
cd env

# Configure git
git clone https://github.com/guywilsonjr/${REPO_NAME}
cd ${REPO_NAME}
git config credential.helper 'cache --timeout=999999'
# git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true
git pull

npm install -g aws-cdk
source ../bin/activate
pip install --upgrade pip
pip install -r requirements.txt --user
cdk --version
cdk bootstrap 936272581790/us-west-2

source reinit.sh

