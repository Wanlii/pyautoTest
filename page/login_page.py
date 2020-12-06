from page.base import BasePage
from selenium.webdriver import ActionChains
import time, random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 创建LoginPage类，继承BasePage类，封装登录页面的基础操作

class LoginPage(BasePage):
    url =
    def name_input(self, name):
        self.by_id("userName").send_keys(name)

    def password_input(self, password):
        self.by_id("password").send_keys(password)

    def login_click(self):
        self.by_id("TencentCaptcha").click()
    # 模拟人的操作轨迹
    def get_tracks(self, distance):
        v = 0
        t = random.randint(2, 3) / 10
        # 位移/轨迹列表，列表内每一个元素代表0.2s的位移
        tracks = []
        current = 0
        # 到达mid值时开始减速
        mid = distance * 4 / 5
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            s = v0 * t + 0.5 * a * (t * t)
            current += s
            tracks.append(round(s))

            v = v0 + a * t
        return tracks

    # 等待滑块出现
    def wait_thumb(self):
        wait_frame = WebDriverWait(self.driver, 10, 0.2).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "tcaptcha_iframe")))
        wait = WebDriverWait(self.driver, 10, 0.2).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='tcaptcha_drag_thumb']")))

    # 拖动滑块直到成功识别
    def move(self):
        L = [204, 210, 223, 231, 213]
        contigo = self.by_xpath("//*[@id='tcaptcha_drag_thumb']")
        print(contigo)
        flag = True
        while flag:
            time.sleep(0.1)
            tracks = self.get_tracks(random.choice(L))
            button = ActionChains(self.driver)
            button.click_and_hold(contigo).perform()
            for x in tracks:
                button.move_by_offset(x, 0).perform()
                button = ActionChains(self.driver)

            button.release(contigo).perform()
            time.sleep(1)
            try:
                self.by_xpath("//*[@id='tcaptcha_drag_thumb']")
                print("to be continued")
            except:
                flag = False
                print("success")