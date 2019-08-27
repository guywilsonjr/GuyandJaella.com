import boto3
import os
import time
import urllib.request

HTTPS = 'https://'
MAIN_SITE_METRIC = ('MainSite', 'Latency', '#FF0000')
SIDEBAR_SITE_METRIC = ('Sidebar', 'Latency', '#1E90FF')
METRICS = {MAIN_SITE_METRIC, SIDEBAR_SITE_METRIC}

def get_static_url_prefix() -> str:
    return '{}{}/'.format(HTTPS, os.environ['STATIC_DOMAIN'])
    

def get_site_url_prefix() -> str:
    return '{}www.{}/'.format(HTTPS, os.environ['SITE_DOMAIN'])
    
def inject(template: str, injections: dict):
    final = template
    for key, value in injections.items():
        final = final.replace(key, value)
    return final


async def fetch_file_txt(file: str, metric: tuple, from_disk=False) -> str:
    if from_disk:
        with open(file, 'r') as txt:
            return txt.read()
    else:
        return await https_get(file=file, metric=metric)
    
def validate_metric():
    validation_errors = {}
    
async def https_get(file: str, metric: tuple) -> str:
    url = '{}{}'.format(get_static_url_prefix(), file)
    name = '{} {} {}'.format(metric[0], metric[1], file)
    start = time.time()
    data = urllib.request.urlopen(url)
    send_metrics(time.time() - start, metric, name)
    data = data.read().decode()
    return data


cloudwatch = boto3.client('cloudwatch')

def send_metrics(time, metric: tuple, name: str):
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

