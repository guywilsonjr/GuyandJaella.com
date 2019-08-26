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
python3 -m venv ${REPO_NAME}Env
${REPO_NAME}Env

# Configure git
git clone https://github.com/guywilsonjr/${REPO_NAME}
cd ${REPO_NAME}
git config credential.helper 'cache --timeout=999999'
# git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true
git pull
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
rm get-pip.py
npm install -g aws-cdk
source ../bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt --user

cdk --version
cdk bootstrap 936272581790/us-west-2

source bin/reinit.sh

domain_name = 'guyandjaella.com'
apex_domain = domain_name
env = {'DOMAIN': apex_domain}
code_txt = None
with open('ensure_ns.py', 'r') as content:
    code_txt = content.read()

r53 = boto3.client('route53')
acm = boto3.client('acm', region_name='us-east-1')

for zone in r53.list_hosted_zones()['HostedZones']:
    zone_name = zone['Name'][:-1]
    if zone_name == apex_domain:
        hosted_zone_id = zone['Id'].partition('/hostedzone/')[2]
        print('HostedZone Found:{}\n{}'.format(zone_name, hosted_zone_id))
        certs = acm.list_certificates(CertificateStatuses=['ISSUED'])[
            'CertificateSummaryList']
        potential_cert_arn = [cert['CertificateArn']
                               for cert in certs if cert['DomainName'] == domain_name]
        if potential_cert_arn:
            cert_arn = potential_cert_arn[0]
            print('Certificate Found:{}'.format(certs))
            full_cert = acm.describe_certificate(CertificateArn=cert_arn)
            print(full_cert)