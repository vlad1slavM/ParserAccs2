from selenium import webdriver
from termcolor import cprint
import colorama


def debug_print(message, color):
    debug = True
    if debug is True:
        cprint(message, color)


class VK_Checker:
    def __init__(self):
        try:
            self.browser = webdriver.PhantomJS()
            debug_print("Browser open - OK", "green")
        except Exception:
            debug_print("!-----Browser not open-----!", "red")
            return 1
        self.browser.get("https://vk.com/login")
        debug_print("Url get - OK", "green")

    def auth(self, login, password):
        self.browser.find_element_by_id("email").send_keys(login)
        self.browser.find_element_by_id("pass").send_keys(password)
        self.browser.find_element_by_id("login_button").click()
        debug_print("Login/password - OK", "green")
        self.browser.get("https://vk.com/login")
        if (self.browser.current_url[:20] == "https://vk.com/login"):
            debug_print("!-----Incorrect password-----!", "red")
            self.browser.close()
            return 3
        else:
            debug_print("Authorization - OK", "green")
            self.browser.close()
            return 0


colorama.init()
login, password = "", ""
vk = VK_Checker()
vk.auth(login, password)
