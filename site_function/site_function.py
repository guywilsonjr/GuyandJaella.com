import json
import os
import urllib.request
import asyncio
import tracemalloc
import logging
import boto3
from typing import List
import time

tracemalloc.start()
HTTPS = 'https://'
logger = logging.getLogger()
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
loop = asyncio.get_event_loop()

METRICS = [('MainSite', 'Latency', '#FF0000'), ('Sidebar', 'Latency', '#1E90FF')]
cloudwatch = boto3.client('cloudwatch')

def send_metrics(time, metric):
    app_name = 'GuyandJaella'
    stage = None
    if 'PROD' in os.environ:
        stage = 'PROD'
    else:
        stage = 'DEV'
    
    cloudwatch.put_metric_data(Namespace=app_name,
        MetricData = [
                {
                    'MetricName': metric[0],
                    'Dimensions': [
                        {
                            'Name': 'By App Version',
                            'Value': os.environ['APP_VERSION']
                        },
                        {
                            'Name': 'By Operation',
                            'Value': metric[1]
                        },
                        {
                            'Name': 'By Stage',
                            'Value': stage
                        },
                    ],
                    'Unit': 'Milliseconds',
                    'Value': time*1000
                },
            ])
    name = '{}.{}'.format(metric[1], metric[2])
    


async def https_get(url: str, metric: tuple) -> str:
    start = time.time()
    data = urllib.request.urlopen(url)
    send_metrics(time.time() - start, metric)
    data = data.read().decode()
    return data


def inject_sidebar_items(
        html: str,
        items: dict,
        item_html_snippet: str) -> str:

    item_html = str()
    for key, value in items.items():
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
        final = final.replace(key, value)
    return final


async def create_html(site_domain, static_domain, template_uri):
    
    sidebar_template_task = asyncio.create_task(https_get('{}sidebar_item.html'.format(get_url_prefix(static_domain)), METRICS[1]))
    main_template_task = asyncio.create_task(https_get(
        '{}{}'.format(get_url_prefix(static_domain), template_uri), METRICS[0]))
            
    sidebar_injections = get_sidebar_injections(static_domain)
    main_injections = get_assets_url_injections(static_domain)

    sidebar_template = await sidebar_template_task
    sidebar = inject(sidebar_template, sidebar_injections)
    side_main_injection = [('{SIDEBAR_ITEMS}', sidebar)]

    main_template = await main_template_task
    main_html = inject(main_template, main_injections)
    html = inject(main_html, side_main_injection)

    return html


def handler(event, context):
    logger.info('EVENT: ', event)

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

if 'DEV' in os.environ:
    handler({}, {})
