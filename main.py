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


def goAmazon():

    ipaddress = os.path.join(os.path.dirname(os.path.abspath(__file__)), "com/ipaddress")
    infoProperties = os.path.join(os.path.dirname(os.path.abspath(__file__)), "com/info.properties")

    ipFile = open(ipaddress, "r")

    properties = Properties(infoProperties)

    for ipLine in ipFile:
        ipLine = ipLine.strip('\n')
        ip = ipLine.split(":")[0]
        port = ipLine.split(":")[1]

        logging.debug("{} ip的操作开始!!!".format(ipLine))

        # options = setChromeOptions(ip, port)
        #
        # driver = webdriver.Chrome(chrome_options=options)

        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server=http://{}".format(ipLine))

        driver = webdriver.Chrome(chrome_options=options)

        # driver.get("http://www.baidu.com")
        # driver.find_element_by_id("kw").send_keys("ip")
        # driver.find_element_by_id("su").click()

        amazonUrl = properties.get("amazonUrl")

        userName = "ssspure@qq.com"

        password = "plmokn321."

        asin = properties.get("asin")

        keyWord = properties.get("keyWord")

        onlyCart = True

        logging.debug("亚马逊地址是:%s,搜索关键词是:%s, ASIN码是:%s", amazonUrl, keyWord, asin)

        loginAmazon = LoginAmazon(driver, amazonUrl, userName, password, asin, keyWord, onlyCart)

        logging.debug("{} ip的操作结束!!!".format(ipLine))


if __name__ == "__main__":
    # 设置日志信息
    setup_logging()
    logging.debug("程序运行开始!!!")
    goAmazon()
    logging.debug("程序运行结束!!!")