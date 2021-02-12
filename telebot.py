from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.types import ChatActions
from aiogram.utils import executor
from aiogram import Bot, types
import configparser


class Origin_Bot:
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
                scr = 'Path' + str(msg.from_user.id)
                with open(scr, 'w') as new_file:
                    new_file.write(msg.text)
                '''
                await check(msg.from_user.id, scr)
                '''

        @self.dp.message_handler(content_types=['document'])
        async def logic_file(msg: types.Message):
            file_info = await self.bot.get_file(msg.document.file_id)
            downloaded_file = await self.bot.download_file(file_info.file_path)
            src = 'D:\\Python\\Origin parser\\' + str(msg.document.file_id)
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file.read())
            '''
            await check(msg.from_user.id, scr)
            '''

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
    async def check(self, user_id, src):
        await self.bot.send_message(user_id, "Ожидайте ваш запрос обрабатывается")
        '''
        parserLog(src) проверка наличия данных об аккаутнах
        if (наличие данных is True):
            if (Origin_checker() == 0) возвращает 0 если успешно
                await self.send_file(msg.from_user.id) отправляет пользователю файл с данными аккаунтов
            elif (Origin_checker() == 1):
                ...
            else:
                ...
        else:
            await self.bot.send_message(msg.from_user.id, self.answer_error)'''


bot = Origin_Bot()
bot.start()
