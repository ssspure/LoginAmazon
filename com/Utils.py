from selenium import webdriver
import time
from selenium.common.exceptions import *
import logging
import os
import yaml
import logging.config


def checkIP(ip):
    """
    通过芝麻代理检测IP时候可用
    :param ip:包含端口号的IP地址。Format:ip:port
    :return:
    """
    result = False
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome(chrome_options=option)
    driver.get("http://h.zhimaruanjian.com/agent/")
    driver.find_element_by_id("check_data").send_keys(ip)
    time.sleep(2)
    driver.find_element_by_id("check").click()
    time.sleep(10)
    try:
        ul = driver.find_element_by_class_name("result_tpl")
        lis = ul.find_elements_by_tag_name("li")

        if (lis[0].text + ":" + lis[1].text) == ip:
            if lis[4].text != "连接超时":
                result = True

    except NoSuchElementException as e:
        pass
    return result


def setup_logging(default_level=logging.DEBUG):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logconfig.ymal")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)