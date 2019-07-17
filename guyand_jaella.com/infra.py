#!/usr/bin/env python3

from aws_cdk import core
from website import WebsiteStack
import os
app = core.App()

WebsiteStack(
    app,
    'GuyandJaella',
    'GuyandJaella.com'
)
app.synth()
