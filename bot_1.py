import logging
import sqlite3
import time

from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup
from aiogram.types.message import ContentType
from datetime import datetime, date
from aiogram import Bot, Dispatcher, executor, types
from db import Database
import os
from dotenv import load_dotenv

# proxy_url = 'http://proxy.server:3128'

PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')



admins = [740124049]

def tel_bot():

    # Объект бота
    bott = Bot(token=os.getenv('TOKEN'))

    # Диспетчер для бота
    bot = Dispatcher(bott)
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)

    @bot.message_handler(commands=["know_id"])
    async def admin(message: types.Message):
        await message.bot.send_message(message.chat.id, f'{message.chat.id}')

    @bot.message_handler(commands=["add_admin"])
    async def admin(message: types.Message):
        db = Database('coffe.db')

        if db.user_exists(message.chat.id, 'admins'):
            await message.bot.send_message(message.chat.id,
                                           'id Например : 25824934')
            db.set_cur_pos(message.chat.id, 'add_admin', 'admins')

    @bot.message_handler(commands=["all"])
    async def admin(message: types.Message):
        db = Database('coffe.db')

        if db.user_exists(message.chat.id, 'admins'):
            all = db.get_all_drinks()
            for item in all:
                await message.bot.send_message(message.chat.id, f'Напиток - {item[0]}\nЦена - {item[6]}\nДобавки - {item[3]}\nМолоко - {item[4]}\nОбьем - {item[2]}\nНаличие - {item[5]}\n')

    @bot.message_handler(commands=["del"])
    async def admin(message: types.Message):
        db = Database('coffe.db')
        if db.user_exists(message.chat.id, 'admins'):
            await message.bot.send_message(message.chat.id, 'Имя напитка Например : Каппучино')
            db.set_cur_pos(message.chat.id, 'del', 'admins')

    @bot.message_handler(commands=["add_drink"])
    async def admin(message: types.Message):
        db = Database('coffe.db')

        if db.user_exists(message.chat.id, 'admins'):
            await message.bot.send_message(message.chat.id,
                                           'Имя.Цена.Обьем и цена.Добавки и цена.Молоко и цена.Наличие(да/нет) Например : Каппучино.100.60_0,120_20,180_40.Сироп_50,Долька апельсина_30.Миндальное_50.да')
            db.set_cur_pos(message.chat.id, 'add_drink', 'admins')

    @bot.message_handler(commands=["admin"])
    async def admin(message: types.Message):
        db = Database('coffe.db')

        if db.user_exists(message.chat.id, 'admins'):
            await message.bot.send_message(message.chat.id,
                                           'Команды\nПросмотр жалоб - /prosmotrzhalob\nДобавить админа - /add_admin'
                                           '\nДобавить напиток - /add_drink'
                                           '\nУдалить напиток - /del'
                                           '\nВывести напитки - /all'
                                           '\nУзнать id - /know_id')

    @bot.message_handler(commands=["start"])
    async def start(message: types.Message):
        db = Database('coffe.db')
        # print(message.chat.username)
        # print(message.message_id)
        if not db.user_exists(message.chat.id, 'admins'):

            if not db.user_exists(message.chat.id, 'users'):
                db.add_user(message.chat.id, 'users')
                db.set_nickname(message.chat.id, f'{message.chat.first_name}', 'users')

        await message.bot.send_message(message.chat.id,
                                       "Привет! 👋🏻\nНажми - /zakaz чтобы выбрать кофе",  reply_markup=types.ReplyKeyboardRemove())

    @bot.message_handler(commands=["prof"])
    async def start(message: types.Message):
        db = Database('coffe.db')
        if db.user_exists(message.chat.id, 'users'):
            name = db.get_name(message.chat.id)
            skidka = db.get_skidka(message.chat.id)
            if skidka != 'None' and skidka != '':
                skidka = skidka.split('.')[1]
            skidka_cur = db.get_skidka_cur(message.chat.id)
            if skidka_cur != 'None' and skidka_cur != '':
                skidka_cur = skidka_cur.split('.')[1]
            sum = db.get_sum(message.chat.id)
            if sum != 'None' and sum != '':
                sum = sum.split('.')[1]
            await message.bot.send_message(message.chat.id, f'Здравстуйте, {name}!\nВы потратили в этом месяце -  {sum}₽\nСкидка в этом месяце - {skidka_cur} %\nСкидка в следующем месяце - {skidka} %\nНажми /love_zakaz чтобы посмотреть любимые заказы')

    @bot.message_handler(commands=["del_love_zakaz"])
    async def start(message: types.Message):
        db = Database('coffe.db')
        if db.user_exists(message.chat.id, 'users'):
            love_zakaz = db.get_love_zakaz(message.chat.id)
            if love_zakaz == 'None' or love_zakaz == '':
                await message.bot.send_message(message.chat.id, 'У вас пока нет любимых заказов. Сделай заказ (/zakaz) и добавь его в любимые!')
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                love_zakaz = love_zakaz.split(';')
                for i in range(len(love_zakaz)):
                    if love_zakaz[i] != '':
                        keyboard.add(f'{i+1}')
                await message.bot.send_message(message.chat.id, 'Выбери номер заказа который хочешь удалить', reply_markup = keyboard)
                db.set_cur_pos(message.chat.id, 'del_love_zakaz', 'users')

    @bot.message_handler(commands=["love_zakaz"])
    async def start(message: types.Message):
        db = Database('coffe.db')
        if db.user_exists(message.chat.id, 'users'):
            love_zakaz = db.get_love_zakaz(message.chat.id)
            if love_zakaz == 'None' or love_zakaz == '':
                await message.bot.send_message(message.chat.id, 'У вас пока нет любимых заказов. Сделай заказ (/zakaz) и добавь его в любимые!')
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

                love_zakaz = love_zakaz.split(';')
                for i in range(len(love_zakaz)):
                    if love_zakaz[i] != '':
                        z = love_zakaz[i].split(':')[1]
                        keyboard.add(f'{i+1}')

                        await message.bot.send_message(message.chat.id,
                                                       f'Заказ № {i+1}\n{z}')
                await message.bot.send_message(message.chat.id, 'Выбери номер заказа который хочешь оплатить\n или нажми /del_love_zakaz чтобы удалить один закзаз', reply_markup = keyboard)
                db.set_cur_pos(message.chat.id, 'nomer_love_zakaz', 'users')

    @bot.message_handler(commands=["zakaz"])
    async def start(message: types.Message):
        db = Database('coffe.db')
        if db.user_exists(message.chat.id, 'users'):
            all = db.get_all_drinks()
            db.set_cur_pos(message.chat.id, 'zakaz', 'users')
            db.set_zakaz(message.chat.id, '')
            db.set_text_admin(message.chat.id, '')

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for item in all:
                keyboard.add(f'{item[0]} - {item[6]}₽')
            await message.bot.send_message(message.chat.id, 'Выберите напиток', reply_markup=keyboard)



    @bot.pre_checkout_query_handler(lambda q: True)
    async def checkout_process(pre_checkout_query: PreCheckoutQuery):
        print(pre_checkout_query.from_user.username)
        await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

        # if pre_checkout_query.from_user.first_name == 'Sergey' or pre_checkout_query.from_user.username == '':

        #     await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message='Nik!')
        # else:

    @bot.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
    async def successful_payment(message: Message):
        db = Database('coffe.db')
        await message.bot.send_message(
            message.chat.id,

            'Платеж на сумму `{total_amount} {currency}` совершен успешно!'.format(
                total_amount=message.successful_payment.total_amount // 100,
                currency=message.successful_payment.currency)
        )
        text_admin = db.get_text_admin(message.chat.id)
        text_admin += f'\n\n{message.chat.first_name}\n{message.chat.last_name}\n{message.chat.username}'
        await message.bot.send_message(740124049, f'Новый заказ\n{text_admin}')
        sum = message.successful_payment.total_amount // 100
        #await message.bot.send_message(740124049, f'{sum}')
        now = date.today()
        month = str(now.month)
        prev_sum = db.get_sum(message.chat.id)
        if month == 12:
            next_month = '01'
        else:
            next_month = str(int(month) + 1)

        if prev_sum == 'None' or prev_sum == '':
            db.set_sum(message.chat.id, f'{month}.{sum}')
            if sum >= 1000:
                db.set_skidka(message.chat.id, f'{next_month}.3')
                await message.bot.send_message(message.chat.id, f'Поздравляем! Ваша скидка на следующий месяц - 3%')
        else:
            if month == prev_sum.split('.')[0]:
                s = int(prev_sum.split('.')[1]) + sum
                if s >= 1000:
                    db.set_skidka(message.chat.id, f'{next_month}.3')
                    await message.bot.send_message(message.chat.id, f'Поздравляем! Ваша скидка на следующий месяц - 3%')

                db.set_sum(message.chat.id, f'{month}.{str(s)}')
            else:
                if sum >= 1000:
                    db.set_skidka(message.chat.id, f'{next_month}.3')
                    await message.bot.send_message(message.chat.id, f'Поздравляем! Ваша скидка на следующий месяц - 3%')

                db.set_sum(message.chat.id, f'{month}.{sum}')
        db.set_cur_pos(message.chat.id, 'love_zakaz', 'users')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(f'Да')
        keyboard.add(f'Нет')

        await message.bot.send_message(message.chat.id, f'Добавить этот заказ в любимые?', reply_markup=keyboard)

    @bot.message_handler(content_types=["text"])
    async def send_text(message: types.Message):

        db = Database('coffe.db')

        if db.user_exists(message.chat.id, 'users'):
            pos = db.get_cur_pos(message.chat.id, 'users')
            if pos == 'zakaz':
                flag = False
                t = message.text.split(' ')[0]
                prev_text_admin = db.get_text_admin(message.chat.id)
                if prev_text_admin == 'None' or prev_text_admin == '':

                    db.set_text_admin(message.chat.id, t)
                else:
                    db.set_text_admin(message.chat.id, f'{prev_text_admin}\n{t}')
                all = db.get_all_drinks()
                for item in all:
                    if t == item[0]:
                        flag = True
                        break
                if flag:
                    prev_zakaz = db.get_zakaz(message.chat.id)
                    db.set_zakaz(message.chat.id, f'{prev_zakaz}{t}')
                    obem = db.get_obem(t).split(',')

                    db.set_cur_pos(message.chat.id, 'obem', 'users')
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

                    for i in range(len(obem)):
                        o = obem[i].split('_')[0]
                        p = obem[i].split('_')[1]
                        keyboard.add(f'{o} мл +{p}₽')

                    await message.bot.send_message(message.chat.id, 'Выберите объем', reply_markup=keyboard)
                else:
                    await message.bot.send_message(message.chat.id, 'Вы ввели не то')

            elif pos == 'obem':
                flag = False
                t = message.text.split(' ')[0]
                prev_text_admin = db.get_text_admin(message.chat.id)
                prev_text_admin += f' {t} мл'
                db.set_text_admin(message.chat.id, prev_text_admin)
                prev_zakaz = db.get_zakaz(message.chat.id)
                n = len(prev_zakaz.split(','))-1
                if n == 0:
                    obem = db.get_obem(prev_zakaz).split(',')
                else:
                    obem = db.get_obem(prev_zakaz.split(',')[n]).split(',')

                for i in range(len(obem)):
                    if t == obem[i].split('_')[0]:
                        obem = obem[i]
                        flag = True
                        break
                if flag:
                    db.set_zakaz(message.chat.id, f'{prev_zakaz}.{obem}')
                    n = len(prev_zakaz.split(',')) - 1
                    if n == 0:
                        moloko = db.get_moloko(prev_zakaz).split(',')
                    else:
                        moloko = db.get_moloko(prev_zakaz.split(',')[n]).split(',')
                    db.set_cur_pos(message.chat.id, 'moloko', 'users')
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

                    if moloko[0] != '':
                        for i in range(len(moloko)):
                            m = moloko[i].split('_')[0]
                            p = moloko[i].split('_')[1]
                            keyboard.add(f'{m} +{p}₽')
                    keyboard.add(f'Обычное +0₽')
                    await message.bot.send_message(message.chat.id, 'Выберите молоко', reply_markup=keyboard)

                else:
                    await message.bot.send_message(message.chat.id, 'Вы ввели не то')

            elif pos == 'moloko':
                flag = False
                t = message.text.split(' ')[0]
                prev_text_admin = db.get_text_admin(message.chat.id)
                prev_text_admin += f' {t} молоко'
                db.set_text_admin(message.chat.id, prev_text_admin)
                prev_zakaz = db.get_zakaz(message.chat.id)
                n = len(prev_zakaz.split(',')) - 1
                if n == 0:
                    name = prev_zakaz.split('.')[0]

                else:
                    zakaz = prev_zakaz.split(',')[n]
                    name = zakaz.split('.')[0]

                moloko = db.get_moloko(name).split(',')
                for i in range(len(moloko)):
                    if t == moloko[i].split('_')[0]:
                        moloko = moloko[i]
                        flag = True
                        break
                if t == 'Обычное':
                    flag = True
                    db.set_zakaz(message.chat.id, f'{prev_zakaz}.Обычное')

                else:
                    db.set_zakaz(message.chat.id, f'{prev_zakaz}.{moloko}')


                if flag:
                    dobavki = db.get_dobavki(name).split(',')
                    db.set_cur_pos(message.chat.id, 'dobavki', 'users')
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    if dobavki[0] != '':
                        for i in range(len(dobavki)):
                            d = dobavki[i].split('_')[0]
                            p = dobavki[i].split('_')[1]
                            keyboard.add(f'{d} +{p}₽')
                    keyboard.add(f'Без добавок +0₽')
                    await message.bot.send_message(message.chat.id, 'Выберите добавки', reply_markup=keyboard)

                else:
                    await message.bot.send_message(message.chat.id, 'Вы ввели не то')

            elif pos == 'dobavki':
                flag = False
                t = message.text.split('+')[0]
                if not t.startswith('Без'):

                    prev_text_admin = db.get_text_admin(message.chat.id)
                    prev_text_admin += f' {t}'
                    db.set_text_admin(message.chat.id, prev_text_admin)
                prev_zakaz = db.get_zakaz(message.chat.id)
                n = len(prev_zakaz.split(',')) - 1
                if n == 0:
                    name = prev_zakaz.split('.')[0]

                else:
                    zakaz = prev_zakaz.split(',')[n]
                    name = zakaz.split('.')[0]
                name = prev_zakaz.split('.')[0]
                dobavki = db.get_dobavki(name).split(',')
                for i in range(len(dobavki)):
                    if dobavki[i].split('_')[0] in t:
                        dobavki = dobavki[i]
                        flag = True
                        break
                if t.startswith('Без'):
                    flag = True
                else:
                    db.set_zakaz(message.chat.id, f'{prev_zakaz}.{dobavki}')



                if flag:
                    db.set_cur_pos(message.chat.id, 'more', 'users')
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(f'Да')
                    keyboard.add(f'Нет')
                    await message.bot.send_message(message.chat.id, 'Добавить еще?', reply_markup=keyboard)

                else:
                    await message.bot.send_message(message.chat.id, 'Вы ввели не то')
            elif pos == 'more':
                t = message.text
                if t == 'Да':
                    all = db.get_all_drinks()
                    db.set_cur_pos(message.chat.id, 'zakaz', 'users')
                    prev_zakaz = db.get_zakaz(message.chat.id)
                    db.set_zakaz(message.chat.id, f'{prev_zakaz},')
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for item in all:
                        keyboard.add(f'{item[0]} - {item[6]}₽')
                    await message.bot.send_message(message.chat.id, 'Выберите напиток', reply_markup=keyboard)
                elif t == 'Нет':
                    db.set_cur_pos(message.chat.id, 'pay', 'users')

                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard.add(f'5')
                    keyboard.add(f'10')
                    keyboard.add(f'15')
                    keyboard.add(f'20')
                    keyboard.add(f'25')
                    keyboard.add(f'30')
                    await message.bot.send_message(message.chat.id, 'Через сколько минут заберете заказ?',reply_markup= keyboard )

                else:
                    await message.bot.send_message(message.chat.id, 'Вы ввели не то')


            elif pos == 'pay':
                try:
                    int(message.text)
                    if int(message.text) < 31:
                        await message.bot.send_message(message.chat.id, 'Ваш заказ :', reply_markup=types.ReplyKeyboardRemove())
                        zakaz = db.get_zakaz(message.chat.id).split(',')
                        text = ''
                        p = 0

                        for i in range(len(zakaz)):

                            z = zakaz[i].split('.')
                            for j in range(len(z)):
                                if j == 0:
                                    price = int(db.get_price(z[j]))
                                    p += price
                                if '_' in z[j]:
                                    p += int(z[j].split('_')[1])

                                    text += z[j].split('_')[0]
                                    text += ' '

                                else:
                                    text += z[j]
                                    text += ' '
                            text += '\n'
                        prev_text_admin = db.get_text_admin(message.chat.id)

                        await message.bot.send_message(message.chat.id, prev_text_admin)
                        await message.bot.send_message(message.chat.id, f'Заберете через {message.text} минут')

                        text_admin = f'{prev_text_admin}\nЧерез {message.text} минут'
                        db.set_text_admin(message.chat.id, text_admin)

                        now = date.today()
                        month = str(now.month)

                        skidka_cur = db.get_skidka_cur(message.chat.id)
                        prev_skidka = db.get_skidka(message.chat.id)

                        if skidka_cur.split('.')[0] == month:
                            prev_skidka = skidka_cur
                        elif prev_skidka.split('.')[0] == month:
                            db.set_skidka_cur(message.chat.id, prev_skidka)
                            db.set_skidka(message.chat.id, '')

                        if prev_skidka != '' and prev_skidka != 'None':
                            if month == prev_skidka.split('.')[0]:
                                skidka = float(prev_skidka.split('.')[1]) * 0.01
                                p = round(float(p) * (1 - skidka))
                                s = prev_skidka.split('.')[1]
                                await message.bot.send_message(message.chat.id, f'Ваша скидка - {s}%')

                        p = str(p) + '00'

                        p = [LabeledPrice(label=f'Готово через {message.text} минут', amount=int(p))]

                        await message.bot.send_invoice(message.chat.id, title='EASY_COFFE', description='Кофе',
                                                       provider_token=PAYMENTS_TOKEN, prices=p,
                                                       currency='rub',

                                                       need_email=False,
                                                       need_phone_number=False,

                                                       start_parameter='example',
                                                       payload='some_invoice')
                    else:
                        await message.bot.send_message(message.chat.id, f'Максимум 30 минут!')
                except:
                    await message.bot.send_message(message.chat.id, f'Вы ввели не то')

            elif pos == 'love_zakaz':
                if message.text == 'Да':
                    prev = db.get_love_zakaz(message.chat.id)
                    zakaz = db.get_zakaz(message.chat.id)
                    text_admin = db.get_text_admin(message.chat.id).split('Через')[0]
                    if f'{zakaz}:{text_admin};' in prev:
                        await message.bot.send_message(message.chat.id, f'Заказ уже есть!', reply_markup=types.ReplyKeyboardRemove())
                    else:

                        if prev == 'None' or prev == '':
                            prev = ''
                            db.set_love_zakaz(message.chat.id, f'{zakaz}:{text_admin};')
                            await message.bot.send_message(message.chat.id, f'Заказ успешно добавлен!', reply_markup=types.ReplyKeyboardRemove())

                        elif len(prev.split(',')) > 5:
                            await message.bot.send_message(message.chat.id, f'Слишком много любимых заказов', reply_markup=types.ReplyKeyboardRemove())
                        else:
                            db.set_love_zakaz(message.chat.id, f'{prev}{zakaz}:{text_admin};')
                            await message.bot.send_message(message.chat.id, f'Заказ успешно добавлен!', reply_markup=types.ReplyKeyboardRemove())
                else:
                    await message.bot.send_message(message.chat.id, f'Ждём вас снова', reply_markup=types.ReplyKeyboardRemove())
                db.set_cur_pos(message.chat.id, '', 'users')
                db.set_zakaz(message.chat.id, '')
                db.set_text_admin(message.chat.id, '')


            elif pos == 'nomer_love_zakaz':
                love_zakaz = db.get_love_zakaz(message.chat.id).split(';')
                try:
                    if int(message.text) <= len(love_zakaz):
                        n = int(message.text) - 1
                        z = love_zakaz[n].split(':')[0]
                        t = love_zakaz[n].split(':')[1]
                        db.set_zakaz(message.chat.id, z)
                        db.set_text_admin(message.chat.id, t)
                        db.set_cur_pos(message.chat.id, 'pay', 'users')

                        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        keyboard.add(f'5')
                        keyboard.add(f'10')
                        keyboard.add(f'15')
                        keyboard.add(f'20')
                        keyboard.add(f'25')
                        keyboard.add(f'30')
                        await message.bot.send_message(message.chat.id, 'Через сколько минут заберете заказ?',
                                                       reply_markup=keyboard)

                    else:
                        db.set_cur_pos(message.chat.id, '', 'users')

                        await message.bot.send_message(message.chat.id, f'Вы ввели не то', reply_markup=types.ReplyKeyboardRemove())
                except:
                    db.set_cur_pos(message.chat.id, '', 'users')
                    await message.bot.send_message(message.chat.id, f'Вы ввели не то', reply_markup=types.ReplyKeyboardRemove())


            elif pos == 'del_love_zakaz':
                love_zakaz = db.get_love_zakaz(message.chat.id)
                love_zakaz_array = love_zakaz.split(';')
                try:
                    if int(message.text) <= len(love_zakaz_array):
                        n = int(message.text) - 1
                        #s = love_zakaz.replace('\n', '')
                        s = love_zakaz.replace(f'{love_zakaz_array[n]};', '')
                        db.set_love_zakaz(message.chat.id, s)
                        await message.bot.send_message(message.chat.id, f'Заказ удален!', reply_markup=types.ReplyKeyboardRemove())
                        db.set_cur_pos(message.chat.id, '', 'users')

                    else:
                        db.set_cur_pos(message.chat.id, '', 'users')

                        await message.bot.send_message(message.chat.id, f'Вы ввели не то', reply_markup=types.ReplyKeyboardRemove())
                except:
                    db.set_cur_pos(message.chat.id, '', 'users')
                    await message.bot.send_message(message.chat.id, f'Вы ввели не то', reply_markup=types.ReplyKeyboardRemove())



        elif db.user_exists(message.chat.id, 'admins'):
            pos = db.get_cur_pos(message.chat.id, 'admins')
            if pos == 'add_admin':
                db.add_user(message.text, 'admins')
                db.set_cur_pos(message.chat.id, '', 'admins')
            elif pos == 'del':
                try:
                    if db.drink_exists(message.text):

                        db.user_del(message.text)
                        await message.bot.send_message(message.chat.id, 'Напиток удален!')
                    else:
                        await message.bot.send_message(message.chat.id, 'Такого нет!')


                except :
                    await message.bot.send_message(message.chat.id, 'Не удалось')
                db.set_cur_pos(message.chat.id, '', 'admins')

            elif pos == 'add_drink':
                t = message.text
                name = t.split('.')[0]
                try:
                    price = t.split('.')[1]
                    obem = t.split('.')[2]
                    dobavki = t.split('.')[3]
                    moloko = t.split('.')[4]
                    nal = t.split('.')[5]
                    db.add_drrink(name)
                    db.set_price(name, price)
                    db.set_dobavki(name, dobavki)
                    db.set_moloko(name, moloko)
                    db.set_nal(name, nal)
                    db.set_obem(name, obem)
                    await message.bot.send_message(message.chat.id, 'Напиток добавился!')
                except :
                    db.user_del(name)
                    await message.bot.send_message(message.chat.id, 'Не удалось')
                db.set_cur_pos(message.chat.id, '', 'admins')

    executor.start_polling(bot, skip_updates=True)
if __name__ == "__main__":
    tel_bot()