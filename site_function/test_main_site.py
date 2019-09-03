import pytest
import json
import os
import asyncio
import site_function
from site_function.site_function import create_html


@pytest.mark.parametrize('static_domain, site_domain, template_uri', [('google.com', 'google.com', '')])
@pytest.mark.asyncio
async def test_create_html(static_domain, site_domain, template_uri):
    await create_html(site_domain, static_domain, template_uri)
    
