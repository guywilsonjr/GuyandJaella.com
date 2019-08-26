import json
import boto3
import os
import asyncio

loop = asyncio.get_event_loop()
r53 = boto3.client('route53')
r53_domains = boto3.client('route53domains', 'us-east-1')


async def get_desired_name_servers(hosted_zone_id: str):
    print('Getting desired')
    return set(r53.get_hosted_zone(
        Id=hosted_zone_id
    )['DelegationSet']['NameServers'])


async def get_actual_name_servers():
    print('Getting Actual')
    return set([ns['Name'] for ns in r53_domains.get_domain_detail(
        DomainName='petdatatracker.com')['Nameservers']])


async def get_name_servers():
    print('Getting All')
    actual_task = asyncio.create_task(get_actual_name_servers())
    desired_task = asyncio.create_task(
        get_desired_name_servers(
            os.environ['HOSTED_ZONE_ID']))
    return await desired_task, await actual_task


def handler(event, context):
    print(event)
    print(context)

    desired_ns, actual_ns = asyncio.run(get_name_servers())
    print('Desired')
    print(desired_ns)
    print('Actual')
    print(actual_ns)
    if actual_ns != desired_ns:
        update_ns = [{'Name': server} for server in desired_ns]
        r53_domains.update_domain_nameservers(
            DomainName=os.environ['DOMAIN'], Nameservers=update_ns)
        return 'UPDATED'
    else:
        return 'MATCHING'
