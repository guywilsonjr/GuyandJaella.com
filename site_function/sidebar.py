import asyncio
import os
if 'DEV' in os.environ:
    from site_function.site_utils import https_get, inject, get_url_prefix
else:
    from site_utils import https_get, inject, get_url_prefix



class Sidebar():
    SIDEBAR_ITEMS = [('Dashboard', 'Dashboard', 'tim-icons icon-image-02'), ('New Snake', 'Snakes', 'tim-icons icon-image-02')]
    def __init__(self, domain: str):
        self.domain = domain
    
    def get_sidebar_item(self, domain: str, title: str, file_path: str, icon: str, item_html_snippet: str) -> list:
        injections = {
            '{LINK}': '{}{}'.format(get_url_prefix(), file_path),
            '{TITLE}': title,
            '{ICON}': icon}
        return inject(item_html_snippet, injections)
        
    async def create_sidebar(self) -> str:
        sidebar_template_task = asyncio.create_task(https_get('{}sidebar_item.html'.format(get_url_prefix()), ('Sidebar', 'Latency', '#1E90FF')))
        self.html = ''
        snippet = await sidebar_template_task
        for title, uri, icon in self.SIDEBAR_ITEMS:
            item = self.get_sidebar_item(self.domain, title, uri, icon, snippet)
            self.html += item
        return self.html
        
    async def get(self) -> str:
        return await self.create_sidebar()

