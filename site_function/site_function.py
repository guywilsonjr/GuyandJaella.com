import os
import asyncio

if 'PROD' in os.environ:
    from main_site import MainSite
else:
    from .main_site import MainSite

status_code = 200
def handler(event, context):
    print(event)
    loop = asyncio.get_event_loop()
    main_site = MainSite()
    site = loop.run_until_complete(
        main_site.create_html(event['resource']))
    data = site
    return {
        "statusCode": status_code,
        "body": data,
        "headers": {
            'Content-Type': 'text/html'
        }
    }
