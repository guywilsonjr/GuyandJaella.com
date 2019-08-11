#!/usr/bin/env python3

from aws_cdk import core
import os
from website import Website
app = core.App()
'''

'''
CERT_ARN = os.environ['SITE_CERT']
HOSTED_ZONE_ID = os.environ['SITE_HOSTED_ZONE_ID']
SITE_DOMAIN = os.environ['SITE_DOMAIN']

Website(
    app,
    'GuyandJaella',
    domain=SITE_DOMAIN,
    cert_arn=CERT_ARN,
    hosted_zone_id=HOSTED_ZONE_ID
)
app.synth()
