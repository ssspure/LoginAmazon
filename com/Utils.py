from selenium import webdriver
import time
from selenium.common.exceptions import *

"""
通过芝麻代理IP检测来查看一个代理IP是否可用
"""


def checkIP(ip):
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