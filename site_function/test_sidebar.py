import pytest
from site_function import sidebar
from site_function.sidebar import Sidebar 
import pytest_asyncio


@pytest.mark.parametrize('domain, title, uri, item_html_snippet', [('abc.com', 'ABC', 'alpha', 'a')])
@pytest.mark.asyncio
async def test_get_sidebar_item(domain: str, title: str, uri: str, item_html_snippet):
    await Sidebar(domain).get()