import os
import asyncio
if 'PROD' in os.environ:
    from site_utils import get_static_url_prefix, fetch_file_txt, inject, MAIN_SITE_METRIC
    from sidebar import Sidebar
else:
    from .site_utils import get_static_url_prefix, fetch_file_txt, inject, MAIN_SITE_METRIC
    from .sidebar import Sidebar



ASSET_REPLACEMENTS = {'assets/': '{}assets/'.format(get_static_url_prefix()),
                      '{UPLOAD_PLACEHOLER}': '{}Images/image_upload.jpg'.format(get_static_url_prefix()),
                      '{GUY_AND_JAELLA_HOME_PIC}': '{}Images/GuyAndJaella.jpg'.format(get_static_url_prefix()),
                      '{API_DOMAIN}': 'api.petdatatracker.com'}



async def create_html(site_domain, static_domain, template_uri) -> str:
    
    main_template_task = asyncio.create_task(fetch_file_txt(file=template_uri, metric=MAIN_SITE_METRIC, from_disk=True))
    sidebar_task = asyncio.create_task(Sidebar(static_domain).get())
    main_injections = ASSET_REPLACEMENTS
    main_template = await main_template_task
    main_html = inject(main_template, main_injections)
    sidebar_html = await sidebar_task

    html = main_html.replace('{SIDEBAR_ITEMS}', sidebar_html)

    return html

HTML_PATH_MAPPINGS = {
    '/': 'home.html',
    '/Dashboard': 'dashboard.html',
    '/Snake/New': 'newSnake.html',
    '/Snakes': 'snakes.html'}


def handler(event, context):
    print(event)
    static_domain = os.environ['STATIC_DOMAIN']
    site_domain = os.environ['SITE_DOMAIN']
    template_uri = HTML_PATH_MAPPINGS[event['resource']]
    status_code = 200
    loop = asyncio.get_event_loop()
    site = loop.run_until_complete(
        create_html(
            site_domain,
            static_domain,
            template_uri))
    return {
        "statusCode": status_code,
        "body": site,
        "headers": {
            'Content-Type': 'text/html',
        }
    }
