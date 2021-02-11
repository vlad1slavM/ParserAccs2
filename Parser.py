import re
import time


class Parser:
    def __init__(self):
        self.a = "login:password"
        self.login_password = {}
        self.login = re.compile("(.+?):")
        self.password = re.compile(':(.+)')

    def test_parser(self):
        start_time = time.time()
        with open('LOG', 'r') as file:
            for line in file:
                login = re.findall(self.login, line)
                password = re.findall(self.password, line)
                self.login_password[login[0]] = password[0]
        print("--- %s seconds ---" % (time.time() - start_time))


parser = Parser()
print(parser.test_parser())
