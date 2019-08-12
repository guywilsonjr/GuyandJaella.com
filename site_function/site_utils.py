import boto3
import os
import time
import urllib.request
HTTPS = 'https://'

def get_url_prefix() -> str:
    return '{}{}/'.format(HTTPS, os.environ['STATIC_DOMAIN'])
    
def inject(template: str, injections: dict):
    final = template
    for injection in injections:
        key = injection[0]
        value = injection[1]
        final = final.replace(key, value)
    return final

    
async def https_get(url: str, metric: tuple) -> str:
    start = time.time()
    data = urllib.request.urlopen(url)
    send_metrics(time.time() - start, metric)
    data = data.read().decode()
    return data


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
