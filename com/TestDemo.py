from com.LoginAmazon import LoginAmazon
from selenium.webdriver.chrome.options import Options
import zipfile
from com.Utils import *
import os
import logging
from com.Properties import Properties


def setChromeOptions(ip, port):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {{
            mode: "fixed_servers",
            rules: {{
              singleProxy: {{
                scheme: "http",
                host: {0},
                port: parseInt({1})
              }},
              bypassList: ["foobar.com"]
            }}
          }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "XXXXXXXXX",
                password: "XXXXXXXXX"
            }}
        }};
    }}
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {{urls: ["<all_urls>"]}},
                ['blocking']
    );
    """.format(ip, port)

    pluginfile = 'proxy_auth_plugin.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    co = Options()
    co.add_argument("--start-maximized")
    co.add_extension(pluginfile)
    return co


ipaddress = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ipaddress")
infoProperties = os.path.join(os.path.dirname(os.path.abspath(__file__)), "info.properties")

ipFile = open(ipaddress, "r")

properties = Properties(infoProperties)

for ipLine in ipFile:
    ipLine = ipLine.strip('\n')
    ip = ipLine.split(":")[0]
    port = ipLine.split(":")[1]

    # options = setChromeOptions(ip, port)
    # driver = webdriver.Chrome(chrome_options=options)

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--proxy-server=http://{}".format(ipLine))
    # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
    driver = webdriver.Chrome(chrome_options=chromeOptions)

    # driver.get("http://www.baidu.com")
    driver.get("http://httpbin.org/ip")
    driver.find_element_by_id("kw").send_keys("ip")
    driver.find_element_by_id("su").click()

    driver.close()
    driver.quit()