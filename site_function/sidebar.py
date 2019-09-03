import asyncio
import os
if 'PROD' in os.environ:
    from site_utils import fetch_file_txt, inject, STATIC_URL_PREFIX, SIDEBAR_SITE_METRIC
else:
    from .site_utils import fetch_file_txt, inject, STATIC_URL_PREFIX, SIDEBAR_SITE_METRIC
    

class Sidebar():
    SIDEBAR_ITEMS = [('Home', '', 'tim-icons icon-bank'),('Dashboard', 'Dashboard', 'tim-icons icon-components'), ('New Snake', 'Snakes/New', 'tim-icons icon-simple-add'), ('Snakes', 'Snakes', 'tim-icons icon-bullet-list-67')]
    def __init__(self, template_uri: str):
        self._template_uri = template_uri
        pass

    
    def get_sidebar_item(self, title: str, uri: str, icon: str, item_html_snippet: str) -> list:
        injections = {
            '{LINK}': '{}{}'.format(STATIC_URL_PREFIX, uri),
            '{TITLE}': title,
            '{ICON}': icon}
        return inject(item_html_snippet, injections)
        
        
    async def create_sidebar(self) -> str:
        sidebar_template_task = asyncio.create_task(fetch_file_txt(file=self._template_uri, metric=SIDEBAR_SITE_METRIC, from_disk=True))
        self.html = ''
        snippet = await sidebar_template_task
        for title, uri, icon in self.SIDEBAR_ITEMS:
            item = self.get_sidebar_item(title, uri, icon, snippet)
            self.html += item
        return self.html
        
    async def get(self) -> str:
        return await self.create_sidebar()

