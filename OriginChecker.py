from selenium import webdriver
from termcolor import cprint
import colorama
import time


def debug_print(message, color):
    debug = True
    if debug is True:
        cprint(message, color)


class Origin_Checker:
    def __init__(self, email, password):
        self.t = time.time()
        debug_print("Open browser " + str(time.time() - self.t), "green")
        self.browser = webdriver.PhantomJS()
        debug_print("Browser open - OK " + str(time.time() - self.t), "green")
        self.email = email
        self.password = password
        self.game_list = []

    def auth_origin(self):
        debug_print("auth_origin start " + str(time.time() - self.t), "green")
        url = "https://www.origin.com/rus/ru-ru/game-library"
        url_login = "https://signin.ea.com/p/originX/login?execution=e855582978s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fdisplay%3DoriginXWeb%252Flogin%26response_type%3Dcode%26release_type%3Dprod%26redirect_uri%3Dhttps%253A%252F%252Fwww.origin.com%252Fviews%252Flogin.html%26locale%3Dru_RU%26client_id%3DORIGIN_SPA_ID"
        self.browser.execute_script('window.open("' + url + '","_blank");')
        debug_print("Open windows - OK " + str(time.time() - self.t), "green")
        self.browser.get(url_login)
        debug_print("Get login url - OK " + str(time.time() - self.t), "green")
        self.browser.set_window_size(1920, 1080)
        self.browser.find_element_by_id("email").send_keys(self.email)
        self.browser.find_element_by_id("password").send_keys(self.password)
        debug_print("Email/Password - OK " + str(time.time() - self.t), "green")
        self.browser.find_element_by_id("logInBtn").click()
        debug_print("Click - OK " + str(time.time() - self.t), "green")
        try:
            error_code = self.browser.find_element_by_xpath("//p[@class='otkinput-errormsg otkc']").text[:13]
            self.browser.close()
            if (error_code == "Ошибка данных"):
                debug_print("!-----Incorrect password-----!", "red")
                return 1
            else:
                debug_print("!-----Origin Error-----!", "red")
                return 2
        except Exception:
            debug_print(self.email + " - Authorization successful " + str(time.time() - self.t), "green")
        return 0

    def get_games(self):
        self.browser.switch_to.window(self.browser.window_handles[1])
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
            self.browser.close()
            return 0
        for i in range(0, len(games)):
            game = games[i].find_element_by_xpath(".//div/a/img").get_attribute("alt")
            self.game_list.append(game)
        self.browser.close()
        debug_print("Browser close - OK " + str(time.time() - self.t), "green")
        return 0


colorama.init()
login, password = "", ""
c = Origin_Checker(login, password)
code = c.auth_origin()
if (code == 0):
    c.get_games()
    print(c.game_list)
