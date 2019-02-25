from selenium import webdriver

from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

def getBrowser():
    #1.创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口
    #browser = webdriver.Firefox(executable_path ="D:/tech/scrapy/geckodriver.exe")
    browser = webdriver.Chrome(executable_path ="D:/tech/scrapy/chromedriver.exe")

    return browser

def getRequest(browser,url):
    #2.通过浏览器向服务器发送URL请求
    try:
        browser.get(url)
        sleep(3)
    except:
        browser.refresh()
    #3.刷新浏览器
    #browser.refresh()

def setBrowserSize(browser,width, height):

    #4.设置浏览器的大小
    browser.set_window_size(width,height)

def clickElement(browser, link_text):
    #5.设置链接内容

    try:
        element = browser.find_element_by_link_text("新闻")
        element.click()
        # element=browser.find_element_by_link_text("习近平的“下团组”时间")
        # element.click()
    except Exception as e:
        print("异常")
def clickElementByPartText(browser, link_text):
    #5.设置链接内容
    flag = True
    try:
        element = browser.find_element_by_partial_link_text(link_text)
        element.click()
        sleep(3)
        # element=browser.find_element_by_link_text("习近平的“下团组”时间")
        # element.click()
    except Exception as e:
        flag = False
        print("异常")

    return flag
def mourseOver(browser, text):
    # 2.定位到要悬停的元素
    element = browser.find_element_by_link_text(text)

    # 3.对定位到的元素执行鼠标悬停操作
    ActionChains(browser).move_to_element(element).perform()

def loadUrls(filepath):
    url_list = []
    f_url = open(filepath, 'r', encoding='UTF-8')
    lines = f_url.readlines()
    for url in lines:
        url_list.append(url.strip())

    return url_list

def saveData(datas, filepath='./out.txt'):
    f_out = open(filepath, 'a', encoding='UTF-8')
    f_out.write('\n'.join(datas))
    f_out.write('\n')
    f_out.close()

def autoOperationChrome4Baidu():
    browser = getBrowser()
    setBrowserSize(browser,1400, 800)
    # 打开百度首页
    getRequest(browser, "https://www.baidu.com/")
    # 点击新闻
    clickElement(browser, "新闻")
    # 后退
    browser.back()
    # 鼠标滑动到设置菜单上面
    mourseOver(browser, "设置")

    browser.find_element_by_id("kw").send_keys("selenium")
    browser.find_element_by_id("su").click()
    sleep(10)

def autoOperationChrome4Sinobook():
    browser = getBrowser()
    setBrowserSize(browser,1400, 800)
    url_list = loadUrls(u"./../data/sinobook_scratch_urls.txt")
    processed_url_list = loadUrls(u'./../data/processed_urls.txt')
    for url in url_list:
        if processed_url_list.__contains__(url):
            continue
        # 打开url
        getRequest(browser, url)
        hasNextPage = True
        datas = []
        while hasNextPage:
            # 读取数据
            #catalog_code = browser.find_element_by_xpath("//form/input[@name='sCid']/@value")
            try:

                catalog_code = browser.find_element_by_name("sCid").get_attribute("value")
                catalog_name = browser.find_element_by_name("sCname").get_attribute("value")
                print(catalog_code)
                print(catalog_name)
                course_list = browser.find_elements_by_xpath("//*[@class='tdbn']/a")

                for i_course_name in course_list:
                    print(i_course_name.text)
                    datas.append('{} {}'.format(catalog_code, i_course_name.text))
                # 点击下一页
                hasNextPage = clickElementByPartText(browser, "下一页")
            except:
                sleep(30)
                browser.refresh()
        # 保持已经处理的url
        saveData([url], './../data/processed_urls.txt')
        # 保存数据
        saveData(datas, './../data/catalog_course.txt')


# autoOperationChrome4Baidu()

autoOperationChrome4Sinobook()

