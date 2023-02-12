import psycopg2
import psycopg2.extras
import qrcode
from pprint import pprint
import random
from PIL import Image, ImageDraw
import os
import schedule


def main_tele_and_qr_maker():

    some_number = random.randint(200, 999)

    ######## Изменить перед отправкой в Docker

    # conn = psycopg2.connect(dbname="")
    conn = psycopg2.connect(dbname="")
    def db_all_employee_for_qr():
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s = "SELECT id, surname, foto FROM employee WHERE status = 'True'"
        cur.execute(s)  # Execute the SQL
        list_users = cur.fetchall()
        return list_users


    list_users = db_all_employee_for_qr()


    #create new qr_code
    for item in list_users:
        for items in item:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            ######## Изменить перед отправкой в Docker

            # qr.add_data(f'http://127.0.0.1:80/show_employee?n1={some_number}&id={item[0]}')
            qr.add_data(f'http://127.0.0.1:5000/show_employee?n1={some_number}&id={item[0]}')
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(f'static/images/qr_today/{item[0]}.png') # сохраняем qr по id сотрудника

    with open('static/images/qr_today/code.txt', 'w') as f:
        f.write(str(some_number))


main_tele_and_qr_maker()

# запуск программы каждые 4 часа, на создание новых qr кодов. Сама функция через поток вызвана в главном main
def qr_code_schedule():
    # schedule.every().day.at("08:05:10").do(main_tele_and_qr_maker)
    # schedule.every(4).hours.do(main_tele_and_qr_maker)
    schedule.every(120).seconds.do(main_tele_and_qr_maker)

    while True:
        schedule.run_pending()


