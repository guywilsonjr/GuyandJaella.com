#!/usr/bin/env python3

from aws_cdk import core
from website import WebsiteStack
from CertStack import CertStack
import os
app = core.App()

WebsiteStack(
    app,
    'GuyandJaella',
    'GuyandJaella.com'
)


CertStack(app, 'dacert', env=core.Environment(region='us-east-1'))
app.synth()
