from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Options_chrome
from selenium.webdriver.firefox.options import Options as Options_firefox
from termcolor import cprint
import colorama
import time
import enum

def debug_print(message, color):
    debug = False
    if debug is True:
        cprint(message, color)


class Answer(enum.Enum):
    success = 0
    incorrect_password = 1
    origin_error = 2
    captcha = 3


class Origin_Checker:
    def __init__(self, email, password, browser_type):
        self.t = time.time()
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
        debug_print("Browser open - OK " + str(time.time() - self.t), "green")
        self.email = email
        self.password = password
        self.game_list = []

    def auth_origin(self):
        debug_print("auth_origin start " + str(time.time() - self.t), "green")
        url_login = "https://signin.ea.com/p/originX/login?execution=e855582978s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fdisplay%3DoriginXWeb%252Flogin%26response_type%3Dcode%26release_type%3Dprod%26redirect_uri%3Dhttps%253A%252F%252Fwww.origin.com%252Fviews%252Flogin.html%26locale%3Dru_RU%26client_id%3DORIGIN_SPA_ID"
        self.browser.execute_script('window.open("' + url_login + '","_blank");')
        debug_print("Open windows - OK " + str(time.time() - self.t), "green")
        self.browser.switch_to.window(self.browser.window_handles[1])
        debug_print("Choise window - OK " + str(time.time() - self.t), "green")
        self.browser.set_window_size(1920, 1080)
        try:
            self.browser.find_element_by_id("email").send_keys(self.email)
        except Exception:
            debug_print("Fucking restart page", "yellow")
            self.browser.get(url_login)
            self.browser.find_element_by_id("email").send_keys(self.email)
        self.browser.find_element_by_id("password").send_keys(self.password)
        debug_print("Email/Password - OK " + str(time.time() - self.t), "green")
        self.browser.find_element_by_id("logInBtn").click()
        debug_print("Click logInBtn - OK " + str(time.time() - self.t), "green")
        try:
            error_code = self.browser.find_element_by_xpath("//p[@class='otkinput-errormsg otkc']").text[:13]
            self.browser.quit()
            if error_code == "Ошибка данных":
                debug_print("!-----Incorrect password-----!", "red")
                return Answer.incorrect_password
            else:
                debug_print("!-----Origin Error-----!", "red")
                return Answer.origin_error
        except Exception:
            try:
                captcha = self.browser.find_element_by_id("form-error-google-recaptcha-missing").click()
                if captcha is None:
                    self.browser.quit()
                    debug_print("!-----CAPTCHA Error----!", "red")
                    return Answer.captcha
            except Exception:
                debug_print(self.email + " - Authorization successful " + str(time.time() - self.t), "green")
                return Answer.success

    def get_games(self):
        url = "https://www.origin.com/rus/ru-ru/game-library"
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.get(url)
        debug_print("Change window - OK " + str(time.time() - self.t), "green")
        while True:
            try:
                self.browser.find_element_by_xpath("//ul[@class='l-origin-gameslist-list']")
                break
            except Exception:
                debug_print("Waiting gamelist...", "yellow")
                pass
        try:
            games = self.browser.find_elements_by_xpath("//li[@class='l-origin-gameslist-item origin-gameslist-item']")
        except Exception:
            debug_print("No Games " + str(time.time() - self.t), "green")
            debug_print("Browser close - OK", "green")
            self.browser.quit()
            return 0
        for i in range(0, len(games)):
            game = games[i].find_element_by_xpath(".//div/a/img").get_attribute("alt")
            self.game_list.append(game)
        self.browser.quit()
        debug_print("Browser close - OK " + str(time.time() - self.t), "green")
        return 0


colorama.init()

'''
login, password = "", ""
c = Origin_Checker(login, password, "Firefox")
code = c.auth_origin()
if (code == 0):
    c.get_games()
    print(c.game_list)
'''
