import pytest
import json
import os
import asyncio
import site_function
from site_function import https_get

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
'''
install selenium
cd/tmp/
wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
chromedriver --version

curl https://intoli.com/install-google-chrome.sh | bash
sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
google-chrome --version && which google-chrome
'''

async def get():
    
    capabilities = DesiredCapabilities.CHROME
    capabilities['loggingPrefs'] = { 'browser':'ALL' }
    driver = webdriver.Chrome()
    print('getting')
    return await driver.get('https://d3fqzsbh169wiu.cloudfront.net/test.html')
    
@pytest.mark.asyncio
async def t_https_get(loop):
    site_task = asyncio.create_task(https_get('https://d3fqzsbh169wiu.cloudfront.net/test.html'))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    driver = await get()

    with open ('{}/test.html'.format(dir_path), 'r') as expected_file:
        site = loop.run_until_complete(site_task)
        assert site == str(expected_file.read())
        
            
    with open ('{}/test_out.html'.format(dir_path), 'w') as expected_file:
        entry = driver.get_log('browser')
        expected_file.write(entry)
            
    
def test_run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(t_https_get(loop))
    
def test_inject():
    pass


def test_create_html():
    pass

