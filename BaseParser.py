import re


class Parser:
    def __init__(self):
        self.login_password = {}
        self.login = re.compile("(.+?):")
        self.password = re.compile(':(.+)')

    def pars(self, path):
        with open(path, 'r') as file:
            for line in file:
                login = re.findall(self.login, line)
                password = re.findall(self.password, line)
                self.login_password[login[0]] = password[0]
