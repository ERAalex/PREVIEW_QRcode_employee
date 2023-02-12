import psycopg2
import psycopg2.extras
import qrcode
from pprint import pprint
import telebot
from telebot import types
import random
import datetime
from PIL import Image, ImageDraw
import os
import schedule
import time




def start_telebot():

    ######## Изменить перед отправкой в Docker

    # conn = psycopg2.connect(dbname="")
    conn = psycopg2.connect(dbname="")
    token = ''
    bot = telebot.TeleBot(token)


    @bot.message_handler(commands=['qr'])  # Объявили ветку для работы по команде <strong>number</strong>
    def phone(message):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Подключаем клавиатуру
        button_phone = types.KeyboardButton(text="Отправить телефон и запросить QR код",
                                            request_contact=True)  # Указываем название кнопки, которая появится у пользователя
        keyboard.add(button_phone)  # Добавляем эту кнопку
        bot.send_message(message.chat.id, 'Номер телефона для QR кода',
                         reply_markup=keyboard)  # Дублируем сообщением о том, что пользователь сейчас отправит боту свой номер телефона (на всякий случай, но это не обязательно)


    @bot.message_handler(content_types=['contact'])  # пользователь решит прислать номер телефона :)
    def contact(message):
        if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
            result_bot = message.contact.phone_number  # Выводим у себя в панели контактные данные.
            pprint(result_bot)

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            s = f"SELECT id FROM employee WHERE telephone = '{result_bot}' AND status = 'True'"
            cur.execute(s)  # Execute the SQL
            list_users = cur.fetchall()

            if list_users == []:
                bot.send_message(message.chat.id, 'По данному номеру QR код отсутствует')

            for item in list_users:
                for items in item:
                    result_path = items

                    im = Image.open(f'static/images/qr_today/{result_path}.png')
                    bot.send_photo(message.chat.id, im)

    bot.polling(none_stop=True)