from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Options_chrome
from selenium.webdriver.firefox.options import Options as Options_firefox
from termcolor import cprint
import colorama
import enum


def debug_print(message, color):
    debug = True
    if debug is True:
        cprint(message, color)


class Answer(enum.Enum):
    success = 0
    incorrect_password = 1


class VK_Checker:
    def __init__(self, login, password, browser_type):
        if browser_type == "Chrome":
            options = Options_chrome()
            options.add_argument("--headless")
            self.browser = webdriver.Chrome(options=options)
        elif browser_type == "Firefox":
            options = Options_firefox()
            options.add_argument("--headless")
            self.browser = webdriver.Firefox(options=options)
        else:
            self.browser = webdriver.PhantomJS()
        self.browser.get("https://vk.com/login")
        debug_print("Url get - OK", "green")
        return Answer.success

    def auth_vk(self):
        self.browser.find_element_by_id("email").send_keys(login)
        self.browser.find_element_by_id("pass").send_keys(password)
        self.browser.find_element_by_id("login_button").click()
        debug_print("Login/password - OK", "green")
        self.browser.get("https://vk.com/login")
        if (self.browser.current_url[:20] == "https://vk.com/login"):
            debug_print("!-----Incorrect password-----!", "red")
            self.browser.close()
            return Answer.incorrect_password
        else:
            debug_print("Authorization - OK", "green")
            self.browser.close()
            return Answer.success


colorama.init()

'''
login, password = "", ""
vk = VK_Checker()
vk.auth(login, password)
'''
