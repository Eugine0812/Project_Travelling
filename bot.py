import gspread
from config import TOKEN, ADMIN
import logging
from keyboard import kb, kb_info_belarus, kb_info_abroad, kb_info_admin, kb_information
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
import sqlite3


logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, block INTEGER);""")
conn.commit()

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key("1rexiBskoge_gVfgRWGyxmRI8wwIwPRk2q2EazU9BHr8")


class Dialog(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()


def send_to_sheet(message):
    list = gc.open_by_key ("1rexiBskoge_gVfgRWGyxmRI8wwIwPRk2q2EazU9BHr8" )
    list.sheet1.append_row([message.from_user.id, message.from_user.username, message.from_user.full_name,
                            message.from_user.is_bot, message.from_user.language_code])


@dp.message_handler(commands=['start'])
async def start(message: Message):
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchone()
    if message.from_user.id == ADMIN:
        await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=kb)
    else:
        if result is None:
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
            entry = cur.fetchone()
            if entry is None:
                cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
                conn.commit()
                await message.answer(f"Добро пожаловать, <b>{message.from_user.first_name}!</b>\n"
                                    "Ниже Вы можете выбрать подходящий для Вас тур и ознакомиться "
                                    "с расписанием предстоящих туров", parse_mode=types.ParseMode.MARKDOWN_V2,  reply_markup=kb_information)

                send_to_sheet(message)
        else:
            await message.answer(f"Добро пожаловать, <b>{message.from_user.first_name}!</b>\n"
                                    "Ниже Вы можете выбрать подходящий для Вас тур и ознакомиться "
                                    "с расписанием предстоящих туров", parse_mode=types.ParseMode.HTML, reply_markup=kb_information)


@dp.message_handler(content_types=['text'], text="Туры по Беларуси")
async def spam(message: Message):
    await message.answer(f"<b>{message.from_user.first_name},</b> выберите туры выходного дня по РБ:", parse_mode=types.ParseMode.HTML, reply_markup=kb_info_belarus)


@dp.message_handler(content_types=['text'], text="Туры за границу")
async def spam(message: Message):
    await message.answer(f"<b>{message.from_user.first_name},</b> выберите туры за границу:", parse_mode=types.ParseMode.HTML, reply_markup=kb_info_abroad)


@dp.message_handler(content_types=['text'], text="Календарь туров")
async def spam(message: Message):
    await message.answer("Для просмотра календаря перейдите по ссылке:-->\n"
                         "https://docs.google.com/spreadsheets/d/e/2PACX-1vRc3rzf-0SY580lMQA2kidCHbr9_Eu-hctYd5EPIGY6DoYiQYliFiWrx-XhCjjq_CxwHtpBfHNNqLGd/pubhtml?gid=293021810&single=true")


@dp.message_handler(content_types=['text'], text="Понравился тур?")
async def spam(message: Message):
    await message.answer(f"<b>{message.from_user.first_name},</b> если уже готовы отправиться в крутое путешествие жмите кнопку ниже,\nесли остались вопросы-->пишите @Eugine88", parse_mode=types.ParseMode.HTML, reply_markup=kb_info_admin)


@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: Message):
    await Dialog.spam.set()
    await message.answer('Напиши текст рассылки')


@dp.message_handler(state=Dialog.spam)
async def start_spam(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await message.answer('Главное меню', reply_markup=kb)
        await state.finish()
    else:
        cur = conn.cursor()
        cur.execute(f'''SELECT user_id FROM users''')
        spam_base = cur.fetchall()
        for z in range(len(spam_base)):
            await bot.send_message(spam_base[z][0], message.text)
            await message.answer('Рассылка завершена', reply_markup=kb)
            await state.finish()


@dp.message_handler(content_types=['text'], text='Добавить в ЧС')
async def handler(message: types.Message, state: FSMContext):
    if message.chat.id == ADMIN:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))
        await message.answer('Введите id пользователя, которого нужно заблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=keyboard)
        await Dialog.blacklist.set()


# banim
@dp.message_handler(state=Dialog.blacklist)
async def proce(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await message.answer('Отмена! Возвращаю назад.', reply_markup=kb)
        await state.finish()
    else:
        if message.text.isdigit():
            cur = conn.cursor()
            cur.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
            result = cur.fetchall()
            if len(result) == 0:
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=kb)
                await state.finish()
            else:
                a = result[0]
                id = a[0]
                if id == 0:
                    cur.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.text}")
                    conn.commit()
                    await message.answer('Пользователь успешно добавлен в ЧС.', reply_markup=kb)
                    await state.finish()
                    await bot.send_message(message.text, 'Ты был забанен Администрацией')
                else:
                    await message.answer('Данный пользователь уже получил бан', reply_markup=kb)
                    await state.finish()
        else:
            await message.answer('Ты вводишь буквы...\n\nВведи ID')


@dp.message_handler(content_types=['text'], text='Убрать из ЧС')
async def handler(message: types.Message, state: FSMContext):
    cur = conn.cursor()
    cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = cur.fetchone()
    if result is None:
        if message.chat.id == ADMIN:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Назад"))
            await message.answer('Введите id пользователя, которого нужно разблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=keyboard)
            await Dialog.whitelist.set()


@dp.message_handler(state=Dialog.whitelist)
async def proc(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Отмена! Возвращаю назад.', reply_markup=kb)
        await state.finish()
    else:
        if message.text.isdigit():
            cur = conn.cursor()
            cur.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
            result = cur.fetchall()
            conn.commit()
            if len(result) == 0:
                await message.answer('Такой пользователь не найден в базе данных.', reply_markup=kb)
                await state.finish()
            else:
                a = result[0]
                id = a[0]
                if id == 1:
                    cur = conn.cursor()
                    cur.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
                    conn.commit()
                    await message.answer('Пользователь успешно разбанен.', reply_markup=kb)
                    await state.finish()
                    await bot.send_message(message.text, 'Вы были разблокированы администрацией.')
                else:
                    await message.answer('Данный пользователь не получал бан.', reply_markup=kb)
                    await state.finish()
        else:
            await message.answer('Ты вводишь буквы...\n\nВведи ID')


@dp.message_handler(content_types=['text'], text='Статистика')
async def handler(message: types.Message, state: FSMContext):
    cur = conn.cursor()
    cur.execute('''select * from users''')
    results = cur.fetchall()
    await message.answer(f'Людей которые когда либо заходили в бота: {len(results)}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
