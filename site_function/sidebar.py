import asyncio
import os
if 'PROD' in os.environ:
    from site_utils import fetch_file_txt, inject, get_site_url_prefix, SIDEBAR_SITE_METRIC
else:
    from .site_utils import fetch_file_txt, inject, get_site_url_prefix, SIDEBAR_SITE_METRIC
    

class Sidebar():
    SIDEBAR_ITEMS = [('Home', '', 'tim-icons icon-bank'),('Dashboard', 'Dashboard', 'tim-icons icon-components'), ('New Snake', 'Snake/New', 'tim-icons icon-simple-add'), ('Snakes', 'Snakes', 'tim-icons icon-bullet-list-67')]
    def __init__(self, domain: str):
        self.domain = domain
    
    def get_sidebar_item(self, domain: str, title: str, uri: str, icon: str, item_html_snippet: str) -> list:
        injections = {
            '{LINK}': '{}{}'.format(get_site_url_prefix(), uri),
            '{TITLE}': title,
            '{ICON}': icon}
        return inject(item_html_snippet, injections)
        
    async def create_sidebar(self) -> str:
        sidebar_template_task = asyncio.create_task(fetch_file_txt(file='sidebar_item.html', metric=SIDEBAR_SITE_METRIC, from_disk=True))
        self.html = ''
        snippet = await sidebar_template_task
        for title, uri, icon in self.SIDEBAR_ITEMS:
            item = self.get_sidebar_item(self.domain, title, uri, icon, snippet)
            self.html += item
        return self.html
        
    async def get(self) -> str:
        return await self.create_sidebar()

