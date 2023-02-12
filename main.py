from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

import psycopg2
import psycopg2.extras
import urllib.request
import os
import threading

from werkzeug.utils import secure_filename

from db_employee import db_all_employee_data, db_add_employee_data, db_delete_employee, db_find_employee
from db_employee import db_edit_employee, db_final_edit_employee, check_data
from qr_code_maker import main_tele_and_qr_maker, qr_code_schedule
from telebot_w import start_telebot



app = Flask(__name__)


app.config['SECRET_KEY'] = ''
if 'SECURITY_PASSWORD_SALT' not in app.config:
    app.config['SECURITY_PASSWORD_SALT'] = app.config['SECRET_KEY']

######## Изменить перед отправкой в Docker

# app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = ''


# Создать объект подключения к базе данных
db = SQLAlchemy(app)


DB_HOST = ""
DB_NAME = ""
DB_USER = ""
DB_PASS = ""

######## Изменить перед отправкой в Docker

# conn = psycopg2.connect(dbname="")
conn = psycopg2.connect(dbname="")

UPLOAD_FOLDER = 'static/images/foto/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'JPG', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/")
def index():
    return render_template('index.html')


# страница с созданием работника + отображение всех сотрудников
@app.route("/all_employee_data")
def all_employee_data():
    result = db_all_employee_data()
    return render_template('employee_data.html', all_data=result)


# поиск сотрудника по фамилии или номеру телефона
@app.route("/find_employee", methods=["POST"])
def find_employee():
    result = db_find_employee()
    return render_template('employee_data.html', all_data=result)


# создание нового работника
@app.route("/add_employee_data_new", methods=["GET", "POST"])
def add_employee_data_new():
    # не смог изолировать этот участок, тк приходится подтягивать переменную app и делаем circular problem
    if request.method == 'POST':
        if 'foto' not in request.files:
            flash('there is no file in form!')
            return redirect(request.url)
        # проверка ввода данных
        if check_data() == True:
            flash('Вы ввели не корректные данные, исправьте ошибку. EspinosaAlex\n')
            return redirect(url_for('all_employee_data'))
        else:
            pass

        file1 = request.files['foto']
        surname = request.form['surname']
        path = os.path.join(app.config['UPLOAD_FOLDER'], f'{surname}' + '.jpg')
        #
        file1.save(path)

        # подключаем модуль с кодом по db.images
        db_add_employee_data(file1)
    return redirect(url_for('all_employee_data'))


# удаление работника
@app.route("/delete_employee/<id>", methods=["POST", "GET"])
def delete_employee(id):
    db_delete_employee(id)
    return redirect(url_for('all_employee_data'))


# открытие данных сотрудника. редактирование
@app.route("/edit_employee/<id>", methods=["GET"])
def edit_employee(id):
    result = db_edit_employee(id)
    return render_template('edit_employee.html', result=result)


@app.route("/edit_employee/<id>", methods=["POST"])
def final_edit_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        if 'foto' not in request.files:
            flash('there is no file in form!')
            return redirect(request.url)
        # проверка ввода данных
        if check_data() == True:
            flash('Вы ввели не корректные данные, исправьте ошибку. EspinosaAlex\n')
            return redirect(url_for('all_employee_data'))
        else:
            pass

        file1 = request.files['foto']
        surname = request.form['surname']
        path = os.path.join(app.config['UPLOAD_FOLDER'], f'{surname}' + '.jpg')
        file1.save(path)

        db_final_edit_employee(id, file1)
    return redirect(url_for('all_employee_data'))

# new_number = main_tele_and_qr_maker()


# открытие данных сотрудника. просто просмотр
@app.route("/show_employee", methods=["GET"])
def show_employee():
    with open('static/images/qr_today/code.txt', 'r') as f:
        final_numb = f.read()

    numb_check = request.args.get('n1')
    id = int(request.args.get('id'))

    if numb_check == final_numb:
        result = db_edit_employee(id)
        return render_template('show_employee.html', result=result)
    else:
        return render_template('index.html')


thr_qr_code = threading.Thread(name='qr_code', target=qr_code_schedule)
thr_tele_bot = threading.Thread(name='telegram_bot', target=start_telebot)

thr_qr_code.start()
thr_tele_bot.start()



# NEW PAGES

@app.route("/contact")
def contact():
    return render_template('contact.html')






if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')

