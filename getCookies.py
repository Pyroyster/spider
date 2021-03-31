from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import pickle
import os
import time
from login import LoginDriver




def getPTACookies():
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)
    url = 'https://pintia.cn/auth/login'
    browser.get(url)
    while True:
        # 在此处自动化
        time.sleep(3)
        new_url = 'https://pintia.cn/problem-sets?tab=0'
        while browser.current_url == new_url:
            PTACookies = browser.get_cookies()
            browser.quit()
            cookies = {}
            for item in PTACookies:
                cookies[item['name']] = item['value']
                outputPath = open('PTACookies.pickle', 'wb')
                pickle.dump(cookies, outputPath)
                outputPath.close()
                return cookies


def readCookies():
    if os.path.exists('PTACookies.pickle'):
        readPath = open('PTACookies.pickle', 'rb')
        PTACookies = pickle.load(readPath)
    else:
        PTACookies = getPTACookies()
    return PTACookies


"""
if __name__ == '__main__':
    PTACookies = readCookies()

    browser.get('https://pintia.cn/problem-sets?tab=0')
    for cookie in PTACookies:
        browser.add_cookie({
            "domain": "pintia.cn",
            "name": cookie,
            "value": PTACookies[cookie],
            "path": '/',
            "expires": None
        })
    browser.get('https://pintia.cn/problem-sets?tab=0')
"""

