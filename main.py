from Parser import Parser
# from VkCheck import VK_Checker
from OriginChecker import Origin_Checker
from termcolor import cprint
from multiprocessing import Pool
import multiprocessing
import time


logins = []
base = Parser()
file_path = "test.base.txt"
base.pars(file_path)
for login in base.login_password:
    logins.append(login)

cores = multiprocessing.cpu_count()
a = []
for i in range(cores):
    a.append(i)
b = [5, 6, 7, 8]


def th(i):
    global logins, base
    login = logins[i]
    password = base.login_password.get(login)
    cprint("Check " + login, "magenta")
    c = Origin_Checker(login, password, "Firefox")
    code = c.auth_origin()
    if (code == 0):
        c.get_games()
        with open("base_check.txt", 'a') as file:
            file.write(f"{login} {password} {c.game_list}" + '\n')


if __name__ == "__main__":
    t = time.time()
    with Pool() as pool:
        th1 = pool.map(th, a)
        th2 = pool.map(th, b)
        pool.close()
        pool.join()
    end = time.time() - t
    cprint(end, "magenta")
