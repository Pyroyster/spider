from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from image_match import distance
from image_match import get_tracks
from image_match import getSlideInstance
import time
import json

USERNAME = '3113596134@qq.com'
PASSWORD = 'wuxinyu2001'


class LoginDriver:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('disable-infobars')
        self.url = 'https://pintia.cn/auth/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD

    def post_form(self):
        input_user = self.browser.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div/div[2]/form/div[1]/div[1]/div/div/div[1]/input')
        input_pw = self.browser.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div/div[2]/form/div[1]/div[2]/div/div/div[1]/input')
        input_user.clear()
        input_pw.clear()
        input_user.send_keys(self.username)
        input_pw.send_keys(self.password)
        self.browser.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[2]/form/div[2]/button/div/div').click()

    def clickVerifyBtn(self):
        verify_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'yidun_tips')))
        verify_btn.click()

    def slideVerifyCode(self):
        slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_slider')))
        ActionChains(self.browser).click_and_hold(slider).perform()
        slider_loc_x = slider.location['x']
        bg_img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_bg-img')))
        icon = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yidun_jigsaw')))
        img_width = bg_img.size['width']
        icon_width = icon.size['width']
        img_tags = self.browser.find_elements_by_tag_name("img")
        img_url = img_tags[3].get_attribute("src")
        icon_url = img_tags[4].get_attribute("src")
        match_x = distance(img_url, icon_url, img_width)
        if match_x == -1:
            raise Exception()

        slider_instance = getSlideInstance(img_width, icon_width, match_x)
        tracks = get_tracks(slider_instance)

        for track in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=track, yoffset=0).perform()
        else:
            ActionChains(self.browser).move_by_offset(xoffset=3, yoffset=0).perform()
            ActionChains(self.browser).move_by_offset(xoffset=-3, yoffset=0).perform()
            time.sleep(0.5)
            ActionChains(self.browser).release().perform()
        cur_loc_x = slider.location["x"]
        if cur_loc_x > slider_loc_x:
            print("success")
            return True
        else:
            print("failed")
            return False

    def tryVerify(self, attempt_times=20):
        self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "yidun_tips__text"), r"向右拖动滑块填充拼图"))
        for attempt in range(attempt_times):
            try:
                if self.slideVerifyCode():
                    return True
            except Exception as e:
                print(e)
                ActionChains(self.browser).release().perform()
                refresh = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "yidun_refresh")))
                refresh.click()
                time.sleep(0.6)
        return False

    def login(self):
        self.browser.get(self.url)
        self.post_form()
        self.tryVerify()




if __name__ == '__main__':
    ldrv = LoginDriver()
    ldrv.login()




