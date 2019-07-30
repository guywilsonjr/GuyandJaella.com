#!/usr/bin/env python3

from aws_cdk import core
import os
from website import Website
app = core.App()
'''

'''
CERT_ARN = os.environ['SITE_CERT']
Website(
    app,
    'GuyandJaella',
    'guyandjaella.com'
)
app.synth()
