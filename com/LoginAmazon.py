from bs4 import BeautifulSoup
import re
from selenium.common.exceptions import *
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=http://8.26.121.214:8080')
# driver = webdriver.Chrome(chrome_options=chrome_options)
# driver = webdriver.Chrome()

class LoginAmazon():

    def __init__(self, driver, amazonUrl, userName, password, asin, keyWord, onlyCart):
        self.driver = driver
        self.amazonUrl = amazonUrl
        self.userName = userName
        self.password = password
        self.asin = asin
        self.keyWord = keyWord
        self.onlyCart = onlyCart

        # 根据amazonUrl来判断是哪个国家的亚马逊
        if amazonUrl.find("co.jp") > 0:
            self.country = 1  # 日本
        else:
            self.country = 2  # 美国

        # 根据是否只是加入购物车来调整访问的地址
        if self.onlyCart:
            self.amazonUrl = self.amazonUrl[0:self.amazonUrl.find("/gp")]


        self.gotoAmazon()

    def gotoAmazon(self):

        try:
            # 请求地址
            self.driver.get(self.amazonUrl)

            if not self.onlyCart:
                # 获取输入用户名的文本框
                elem = self.driver.find_element_by_name("email")
                elem.send_keys(self.userName)
                # 输入完用户名之后点击"Continue"按钮
                self.driver.find_element_by_id("continue").click()

                # 获取输入密码的文本框
                elem = self.driver.find_element_by_name("password")
                elem.send_keys(self.password)
                # 输入完密码之后点击登录(signInSubmit)按钮
                self.driver.find_element_by_id("signInSubmit").click()

            time.sleep(10)

            # 输入搜索关键字
            elem = self.driver.find_element_by_name("field-keywords")
            elem.send_keys(self.keyWord)
            # 点击搜索按钮
            element = self.driver.find_element_by_xpath("//input[@type='submit']")
            element.click()

            pageNum = 1

            founded = False

            while True:
                time.sleep(5)

                # 进入产品页面之后获取页面代码
                html = self.driver.page_source

                soup = BeautifulSoup(html, "lxml")

                products = soup.find_all('li', attrs={'id': re.compile(r"result_\d")})

                randNum = random.randint(0, 10)

                # 随机点击别人产品
                if len(products) <= randNum:
                    randNum = 0

                product = products[randNum]
                self.moveToProduct(product)
                if self.country == 1:
                    self.closeJapanWindow()
                else:
                    self.driver.back()

                # 进入产品页面之后获取页面代码
                html = self.driver.page_source

                for product in products:
                    asinTemp = product["data-asin"]
                    if asinTemp == self.asin:
                        founded = True

                        self.moveToProduct(product)
                        break

                # 如果如果已经找到了对应的产品
                if founded:
                    break
                else:
                    # 获取下一页
                    try:
                        nextPage = self.driver.find_element_by_id("pagnNextString")
                        nextPage.click()
                    except Exception as e:
                        break

                    pageNum = pageNum + 1

            if founded:
                if self.country == 1:
                    handles = list(self.driver.window_handles)
                    self.driver.switch_to_window(handles[1])

                # 添加到购物车
                self.addToCart()

                if not self.onlyCart:
                    # 点击加入收藏
                    self.addToLikeList()

                if self.country == 1:
                    self.driver.close()
                    self.driver.switch_to_window(handles[0])

        except Exception as e:
            print(e.with_traceback())
        finally:

            if self.country == 2:
                self.driver.back()

            # 在结束之前，随便点击一个别人的产品
            randNum = random.randint(0, 10)

            # 随机点击别人产品
            if len(products) <= randNum:
                randNum = 0

            product = products[randNum]
            self.moveToProduct(product)
            self.driver.back()

            self.driver.close()

            self.driver.quit()


    def addToLikeList(self):
        """
        将产品添加到收藏列表
        :param self.driver: 浏览器驱动
        :return:
        """
        # 点击加入喜欢按钮

        y = self.driver.find_element_by_id("add-to-wishlist-button-submit").location['y']
        self.driver.execute_script("window.scrollTo(0, {})".format(y))

        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "add-to-wishlist-button-submit")))
        element.click()
        time.sleep(5)
        try:
            element = self.driver.find_element_by_xpath("//div[@class='a-form-actions']")
            button = element.find_elements_by_class_name("a-button-input")[1]
        except NoSuchElementException as e:
            button = self.driver.find_element_by_id("WLHUC_continue")
        button.click()


    def addToCart(self):
        """
        将产品添加到购物车
        :return:
        """
        button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "add-to-cart-button")))
        # button = self.driver.find_element_by_id("add-to-cart-button")
        y = self.driver.find_element_by_id("add-to-cart-button").location['y']
        self.driver.execute_script("window.scrollTo(0, {})".format(y))
        button.click()
        self.driver.back()
        time.sleep(5)


    def moveToProduct(self, product):
        """
        跳转到产品页面
        :param product:
        :return:
        """

        # 获取产品的id
        id = product.get("id")
        # 通过selenium来获取元素
        pro = self.driver.find_element_by_id(id)

        y = self.driver.find_element_by_id(id).location['y']

        self.driver.execute_script("window.scrollTo(0, {})".format(y))

        try:
            # 获取文本链接
            h2 = product.find("h2")
            # 获取文本链接的标题
            title = h2['data-attribute']
            # 点击文本链接,跳转到产品页面
            link = self.driver.find_element_by_link_text(title)
        except NoSuchElementException as e:
            # 某些产品的名称文本没有全部显示出来，这样在匹配的时候就会出错，
            # 所以在出错的时候通过点击评分来迁移换面
            a = pro.find_element_by_class_name("a-size-small")
            link = pro.find_element_by_link_text(a.text)

        link.click()


    def closeJapanWindow(self):

        ids = ["a-autoid-23", "add-to-cart-button", "add-to-wishlist-button-submit"]
        index = random.randint(0, 2)
        id = ids[index]

        handles = list(self.driver.window_handles)
        self.driver.switch_to_window(handles[1])
        element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, id)))
        y = element.location['y']
        self.driver.execute_script("window.scrollTo(0, {})".format(y))

        time.sleep(5)
        self.driver.close()
        self.driver.switch_to_window(handles[0])