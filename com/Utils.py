from selenium import webdriver
import time
from selenium.common.exceptions import *
import logging
import os
import yaml
import logging.config
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def checkIP(ip, browser):
    """
    通过芝麻代理检测IP时候可用
    :param ip:包含端口号的IP地址。Format:ip:port
    :return:
    """
    browser = "chrome"
    result = False
    if browser == "chrome":
        option = webdriver.ChromeOptions()
        # option.add_argument("headless")
        driver = webdriver.Chrome(chrome_options=option)
    elif browser == "firefox":
        # driver = webdriver.Firefox(capabilities={"marionette": False})
        driver = webdriver.Firefox()

    try:
        driver.get("http://h.zhimaruanjian.com/agent/")
        driver.find_element_by_id("check_data").send_keys(ip)
        time.sleep(2)
        btn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "check")))
        btn.click()
        time.sleep(10)
        ul = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "result_tpl")))
        # ul = driver.find_element_by_class_name("result_tpl")
        lis = ul.find_elements_by_tag_name("li")

        if (lis[0].text + ":" + lis[1].text) == ip:
            if lis[4].text != "连接超时":
                result = True

    except Exception as e:
        result = True
        logging.debug("芝麻代理IP检测失败!!!")
    finally:
        if driver is not None:
            driver.close()

    return result


def setup_logging(default_level=logging.DEBUG):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logconfig.ymal")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def setBrowser(ip, browser):
    if browser == "firefox":
        HOST = ip.split(":")[0]
        PORT = ip.split(":")[1]
        def my_proxy(PROXY_HOST,PROXY_PORT):
                fp = webdriver.FirefoxProfile()
                # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
                fp.set_preference("network.proxy.type", 1)
                fp.set_preference("network.proxy.http",PROXY_HOST)
                fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
                fp.set_preference("network.proxy.ssl",PROXY_HOST)
                fp.set_preference("network.proxy.ssl_port",int(PROXY_PORT))
                fp.set_preference("general.useragent.override","whater_useragent")
                fp.update_preferences()
                return webdriver.Firefox(firefox_profile=fp)

        driver = my_proxy(HOST, PORT)
    elif browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server=http://{}".format(ip))

        driver = webdriver.Chrome(chrome_options=options)
    return driver


def checkScrapeProxyIP(ip, driver):
    """
    检测代理IP地址爬虫实际使用的IP是否一致
    :param ip: ip地址
    :param driver: 浏览器对象
    :return:
    """
    proxyIP = ""
    checkedProxyIP = False
    try:
        driver.get("http://httpbin.org/ip")
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "objectBox")))
        proxyIP = element.text.strip('"')
        checkedProxyIP = True
    except Exception as e:
        logging.debug("通过访问http://httpbin.org/ip验证代理IP失败,开始通过百度检测验证代理IP")

        try:
            driver.get("https://www.baidu.com/")
            driver.find_element_by_id("kw").send_keys("ip")
            driver.find_element_by_id("su").click()

            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "c-gap-right")))

            proxyIP = element.text.split(" ")[1]
            checkedProxyIP = True
        except Exception as e:
            logging.debug("通过百度检测验证代理IP失败")
    finally:
        pass
        # driver.close()

    if ip == proxyIP:
        result = True
    else:
        result = False

    return result, checkedProxyIP

