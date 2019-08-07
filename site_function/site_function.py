import json
import os
import urllib.request
import asyncio
import tracemalloc
import logging
from typing import List

tracemalloc.start()
HTTPS = 'https://'
logger = logging.getLogger()
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

async def https_get(url: str) -> str:
    print('URL: {}'.format(url))
    return urllib.request.urlopen(url).read().decode()


def inject_sidebar_items(
        html: str,
        items: dict,
        item_html_snippet: str) -> str:

    item_html = str()
    for key, value in items.items():
        print('KEY: ', key)
        print('Value: ', value)
        item_html = item_html + inject_item_info(item_html_snippet, items)

    return html.replace('{SIDEBAR_ITEMS}', item_html)


def get_url_prefix(domain: str) -> str:
    return '{}{}/'.format(HTTPS, domain)


def get_sidebar_injections(domain: str) -> list:
    return [('{LINK}', '{}dashboard.html'.format(get_url_prefix(domain))),
            ('{TITLE}', 'Dashboard')]


def get_assets_url_injections(domain: str) -> list:
    return [('assets/', '{}assets/'.format(get_url_prefix(domain)))]

def get_side_main_injection(sidebar_template: str) -> list:
    return inject(sidebar_template, sidebar_injections)
    
def inject(template: str, injections: dict):
    final = template
    for injection in injections:
        key = injection[0]
        value = injection[1]
        print('KEY: ', key)
        print('Value: ', value)
        final = final.replace(key, value)
    return final


async def create_html(domain, template_uri):
    sidebar_template_task = asyncio.create_task(https_get('{}sidebar_item.html'.format(get_url_prefix(domain))))
    main_template_task = asyncio.create_task(https_get(
        '{}{}'.format(get_url_prefix(domain), template_uri)))
            
    sidebar_injections = get_sidebar_injections(domain)
    main_injections = get_assets_url_injections(domain)

    sidebar_template = await sidebar_template_task
    sidebar = inject(sidebar_template, sidebar_injections)
    print('sidebar: {}'.format(sidebar))
    side_main_injection = [('{SIDEBAR_ITEMS}', sidebar)]

    main_template = await main_template_task
    main_html = inject(main_template, main_injections)
    html = inject(main_html, side_main_injection)

    return html


def handler(event, context):
    logger.info('EVENT: ', event)

    domain = os.environ['STATIC_DOMAIN']
    template_uri = os.environ['TEMPLATE_URI']
    status_code = 200

    loop = asyncio.get_event_loop()
    site = loop.run_until_complete(create_html(domain, template_uri))

    return {
        "statusCode": status_code,
        "body": site,
        "headers": {
            'Content-Type': 'text/html',
        }
    }


print(handler({}, {}))
