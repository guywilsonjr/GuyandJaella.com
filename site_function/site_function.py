import os
import urllib.request
import asyncio
import boto3
from typing import List
import time
if 'DEV' in os.environ:
    from site_function.site_utils import get_url_prefix, https_get, inject
    from site_function.sidebar import Sidebar
else:
    from site_utils import get_url_prefix, https_get, inject
    from sidebar import Sidebar

loop = asyncio.get_event_loop()


ASSET_REPLACEMENTS = [('assets/', '{}assets/'.format(get_url_prefix()))]
METRICS = [('MainSite', 'Latency', '#FF0000'), ('Sidebar', 'Latency', '#1E90FF')]


async def create_html(site_domain, static_domain, template_uri):
    main_template_task = asyncio.create_task(https_get(
        '{}{}'.format(get_url_prefix(), template_uri), ('MainSite', 'Latency', '#FF0000')))
    
    main_injections = ASSET_REPLACEMENTS
    main_template = await main_template_task
    main_html = inject(main_template, main_injections)
    sidebar = await Sidebar(static_domain).get()

    html = main_html.replace('{SIDEBAR_ITEMS}', sidebar)

    return html


def handler(event, context):
    static_domain = os.environ['STATIC_DOMAIN']
    site_domain = os.environ['SITE_DOMAIN']
    template_uri = os.environ['TEMPLATE_URI']
    status_code = 200
    site = loop.run_until_complete(create_html(site_domain, static_domain, template_uri))
    return {
        "statusCode": status_code,
        "body": site,
        "headers": {
            'Content-Type': 'text/html',
        }
    }

