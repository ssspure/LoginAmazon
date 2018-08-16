from com.LoginAmazon import LoginAmazon
from com.Utils import *
import os
import logging
from com.Properties import Properties


def goAmazon():

    ipaddress = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config/ipaddress")
    infoProperties = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config/info.properties")

    ipFile = open(ipaddress, "r")

    properties = Properties(infoProperties)
    browser = properties.get("browser")

    for ipLine in ipFile:
        ipLine = ipLine.strip('\n')

        # 检测IP地址是否有效
        #result = checkIP(ipLine, browser)

        result = True

        if result:
            logging.debug("*********{}代理IP开始运行***********".format(ipLine))

            # 根据info.properties中的browser的值，来设置浏览器选项
            driver = setBrowser(ipLine, browser)

            # 检测爬虫使用的代理IP地址是否和提供的代理IP地址一致
            result, checkedProxyIP = checkScrapeProxyIP(ipLine.split(":")[0], driver)

            # 0表示代理IP和爬虫实际使用的IP不一致
            # 1表示代理IP和爬虫实际使用的IP一致
            # 2表示没有验证代理IP和爬虫实际使用的IP是否一致
            execute = 0

            if checkedProxyIP:
                if result:
                    logging.debug("代理IP和爬虫实际使用的IP一致!!!")
                    execute = 1
                else:
                    logging.debug("代理IP和爬虫实际使用的IP不一致!!!")
                    execute = 0
            else:
                logging.debug("代理IP和爬虫实际使用的IP检测失败!!!")
                execute = 2

            if execute != 0:
                # 亚马逊地址
                amazonUrl = properties.get("amazonUrl")

                # 用户账号
                userName = "ssspure@qq.com"

                # 用户密码
                password = "plmokn321."

                # asin码
                asin = properties.get("asin")

                # 搜索关键字
                keyWord = properties.get("keyWord")

                # 是否只添加到购物车
                onlyCart = True

                logging.debug("亚马逊地址是:%s,搜索关键词是:%s, ASIN码是:%s", amazonUrl, keyWord, asin)

                # 根据info.properties中的browser的值，来设置浏览器选项
                driver = setBrowser(ipLine, browser)
                try:
                    loginAmazon = LoginAmazon(driver, amazonUrl, userName, password, asin, keyWord, onlyCart)
                except:
                    # 在发生错误的情况下，判断该产品是否已经添加到购物车
                    if loginAmazon.addedToCart:
                        logging.debug("ERROR:虽然发生了错误,但是该产品已经添加到购物车!!!")
                    else:
                        logging.debug("ERROR:发生了错误,并且该产品没有添加到购物车!!!")
                finally:
                    logging.debug("*********{}代理IP运行结束***********".format(ipLine))
        else:
            logging.debug("%s 代理IP不可用", ipLine)


if __name__ == "__main__":
    # 设置日志信息
    setup_logging()
    logging.debug("-------------------------------程序运行开始-------------------------------")
    goAmazon()
    logging.debug("-------------------------------程序运行结束-------------------------------")