import asyncio
import os
from site_utils import https_get, inject, get_static_url_prefix, get_site_url_prefix



class Sidebar():
    SIDEBAR_ITEMS = [('Dashboard', 'Dashboard', 'tim-icons icon-components'), ('New Snake', 'Snakes', 'tim-icons icon-simple-add')]
    def __init__(self, domain: str):
        self.domain = domain
    
    def get_sidebar_item(self, domain: str, title: str, uri: str, icon: str, item_html_snippet: str) -> list:
        injections = {
            '{LINK}': '{}{}'.format(get_site_url_prefix(), uri),
            '{TITLE}': title,
            '{ICON}': icon}
        return inject(item_html_snippet, injections)
        
    async def create_sidebar(self) -> str:
        sidebar_template_task = asyncio.create_task(
            https_get('{}sidebar_item.html'.format(
                get_static_url_prefix()
                ), ('Sidebar', 'Latency', '#1E90FF'), 'SidebarLatency'))
        self.html = ''
        snippet = await sidebar_template_task
        for title, uri, icon in self.SIDEBAR_ITEMS:
            item = self.get_sidebar_item(self.domain, title, uri, icon, snippet)
            self.html += item
        return self.html
        
    async def get(self) -> str:
        return await self.create_sidebar()

