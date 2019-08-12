import urllib.request
import os


def handler(event, context):
    data = urllib.request.urlopen('https://guyandjaella.com')
     