#!/usr/bin/env python3

from aws_cdk import core
import os
from website import Website
app = core.App()
'''

'''
SITE_DOMAIN = os.environ['SITE_DOMAIN']

Website(
    app,
    'GuyandJaella',
    domain=SITE_DOMAIN
)
app.synth()
