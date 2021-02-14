from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.types import ChatActions
from aiogram.utils import executor
from aiogram import Bot, types
from MainChecker import MultiprocessChecker as MC
from BaseParser import Parser
import configparser


class Telegram_Bot:
    def __init__(self):
        self.read_config(self)
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot)

    def start(self):
        @self.dp.message_handler(commands=['start'])
        async def process_start_command(message: types.Message):
            button_one = KeyboardButton("Загрзить базу сообщением")
            button_two = KeyboardButton("Загрузить базу из файла")
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(button_one)
            keyboard.add(button_two)
            await message.reply(self.hello, reply_markup=keyboard)

        @self.dp.message_handler(commands=['help'])
        async def process_help_command(message: types.Message):
            await message.reply(self.help)

        @self.dp.message_handler()
        async def logic_text(msg: types.Message):
            print(msg.text)
            if (msg.text == "Загрзить базу сообщением"):
                await self.bot.send_message(msg.from_user.id, self.answer_text)
            elif (msg.text == "Загрузить базу из файла"):
                await self.bot.send_message(msg.from_user.id, self.answer_file)
            else:
                scr = 'Base_' + str(msg.from_user.id) + ".txt"
                with open(scr, 'w') as new_file:
                    new_file.write(msg.text)
                await self.check(self, msg.from_user.id, scr, "Origin")  # доработать

        @self.dp.message_handler(content_types=['document'])
        async def logic_file(msg: types.Message):
            file_info = await self.bot.get_file(msg.document.file_id)
            downloaded_file = await self.bot.download_file(file_info.file_path)
            src = str(msg.document.file_id)
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file.read())
            await self.check(msg.from_user.id, scr, "Origin")  # доработать

        executor.start_polling(self.dp)

    @staticmethod
    def read_config(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.hello = config.get("Text", "hello")
        self.help = config.get("Text", "help")
        self.answer_text = config.get("Text", "answer_text")
        self.answer_file = config.get("Text", "answer_file")
        self.answer_error = config.get("Text", "not_found")
        self.token = config.get("Token", "token")

    @staticmethod
    async def send_file(self, user_id):
        f = open("test.txt", 'rb')
        await self.bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT)
        await self.bot.send_document(user_id, f)
        f.close()

    @staticmethod
    async def check(self, user_id, src, type_base):
        await self.bot.send_message(user_id, "Ожидайте ваш запрос обрабатывается")
        base = Parser()
        code = 0
        base.pars(src)  # проверка наличия данных об аккаутнах
        if (code == 0):
            checker = MC(base, type_base)
            code = checker.multicheck()
            if (code == 0):
                await self.send_file(msg.from_user.id)  # отправляет пользователю файл с данными аккаунтов
            else:
                await self.bot.send_message(msg.from_user.id, "В базе нет активных аккаунтов")
        else:
            await self.bot.send_message(msg.from_user.id, self.answer_error)


bot = Telegram_Bot()
bot.start()
