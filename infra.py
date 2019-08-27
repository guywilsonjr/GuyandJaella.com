#!/usr/bin/env python3

from aws_cdk.core import App
import os
from website import Website
app = App()

Website(
    app,
    'GuyandJaella',
    domain='guyandjaella.com'
)
app.synth()
