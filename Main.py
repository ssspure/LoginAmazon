from com.LoginAmazon import LoginAmazon
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile
import time
from com.Utils import *
import os


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


def goAmazon():

    ipaddress = os.path.join(os.path.dirname(os.path.abspath(__file__)), "com/ipaddress")

    ipFile = open(ipaddress, "r")

    for ipLine in ipFile:
        ipLine = ipLine.strip('\n')
        result = checkIP(ipLine)

        if not result:
            print("{}不可用".format(ipLine))

        if result:
            print("{}可用".format(ipLine))
            ip = ipLine.split(":")[0]
            port = ipLine.split(":")[1]

            options = setChromeOptions(ip, port)

            driver = webdriver.Chrome(chrome_options=options)

            amazonUrl = r"https://www.amazon.com/gp/sign-in.html"

            userName = "ssspure@qq.com"

            password = "plmokn321."

            asin = "B07DMF5B6Y"

            keyWord = "bark collar"

            onlyCart = True

            loginAmazon = LoginAmazon(driver, amazonUrl, userName, password, asin, keyWord, onlyCart)

if __name__ == "__main__":
    goAmazon()