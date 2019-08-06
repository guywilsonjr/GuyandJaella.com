#!/usr/bin/env python3

from aws_cdk import core
import os
from website import Website
app = core.App()
'''

'''
CERT_ARN = os.environ['SITE_CERT']
HOSTED_ZONE_ID = os.environ['SITE_HOSTED_ZONE_ID']
Website(
    app,
    'GuyandJaella',
    domain='guyandjaella.com',
    cert_arn=CERT_ARN,
    hosted_zone_id=HOSTED_ZONE_ID
)
app.synth()
