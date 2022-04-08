import sqlite3
from aiogram import Dispatcher, Bot, executor
import asyncio
from aiogram.types import Message


admin_id = '481317616'
bot = Bot(token='5202363229:AAF7mjgOEx_ySSQY9C-akum5qRRcguqpiDI', parse_mode='HTML')
dp = Dispatcher(bot=bot)
loop = asyncio.get_event_loop()


async def start_message(dp):
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


@dp.message_handler(commands="help")
async def cmd_help(message: Message):
    await message.answer("Я пока не умею помогать... Я только ваше эхо.")


@dp.message_handler(commands='set_timer')
async def cmd_set(message: Message):
    timer = message.get_args()
    await asyncio.sleep(int(timer))
    await message.answer('TIME LEFT')


@dp.message_handler(commands="start")
async def check_referrals(message: Message):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    r = cur.execute("SELECT id FROM alal").fetchall()
    flag = False
    for i in r:
        if message.from_user.id in i:
            flag = True
    if not flag:
        add = """INSERT INTO alal (id, text, text1)
         values(?, ?, ?)"""
        cur.execute(add, (message.from_user.id, '', ''))
        con.commit()
    await message.answer('/text1_show\n'
                         '/text2_show\n'
                         '/text1 [аргумент]\n'
                         '/text2 [аргумент]')


@dp.message_handler(commands=["text2"])
async def check_referrals(message: Message):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    add = f"""UPDATE alal SET text1 = "{message.get_args()}" WHERE id == {message.from_user.id}"""
    cur.execute(add)
    con.commit()
    await message.answer('OK')


@dp.message_handler(commands=["text1"])
async def check_referrals(message: Message):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    add = f"""UPDATE alal SET text = "{message.get_args()}" WHERE id == {message.from_user.id}"""
    cur.execute(add)
    con.commit()
    await message.answer('OK')


@dp.message_handler(commands=["text1_show"])
async def check_referrals(message: Message):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    r = cur.execute(f"""SELECT text FROM alal
                    WHERE id = {message.from_user.id}""").fetchall()
    text = ''
    for i in r:
        text += i[0]
    con.close()
    if text != '':
        await message.answer(text)
    else:
        await message.answer('ты нихера не писал')


@dp.message_handler(commands=["text2_show"])
async def add_money(message: Message):
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    r = cur.execute(f"""SELECT text1 FROM alal
                WHERE id = {message.from_user.id}""").fetchall()
    text = ''
    for i in r:
        text += i[0]
    con.close()
    if text != '':
        await message.answer(text)
    else:
        await message.answer('ты нихера не писал')


@dp.message_handler()
async def echo(message: Message):
    text = f'Я получил сообщение {message.text}'
    await message.answer(text=text)


def main():
    executor.start_polling(dp, on_startup=start_message)


if __name__ == '__main__':
    main()
