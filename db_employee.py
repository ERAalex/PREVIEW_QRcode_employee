import psycopg2
import psycopg2.extras
from flask import request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from db_create_tables import Employee
import os

######## Изменить перед отправкой в Docker

# conn = psycopg2.connect(dbname="")
conn = psycopg2.connect(dbname="")


def check_data():
    prohibited_list = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '.', '+', '-', ' ', ',']
    name = request.form['name']
    surname = request.form['surname']
    position = request.form['position']
    foto = request.files['foto']
    for item in prohibited_list:
        if item in (name + surname):
            return True
        else:
            pass



def db_all_employee_data():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM employee ORDER by surname"
    cur.execute(s)  # Execute the SQL
    list_users = cur.fetchall()
    return list_users

def db_find_employee():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        surname1 = request.form['surname']
        telephone1 = request.form['telephone']
        surname = "'" + surname1 + "'"
        telephone = "'" + telephone1 + "'"
        cur.execute(f'SELECT * FROM employee WHERE surname = {surname} or telephone = {telephone}')
        res = cur.fetchall()

        return res

def db_add_employee_data(file1):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #
    # # сохраняем названия файлов для их поиска плюс сразу прописываем в имя файла весь путь, для href html

    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    position = request.form['position']
    telephone = request.form['telephone']
    foto = 'static/images/foto/' + f'{surname}.jpg'

    if request.form.get('check_false') == 'on':
        status = False
    elif request.form.get('check_true') == 'on':
        status = True

    cur.execute("""INSERT INTO employee (
    name, surname, email, position, telephone, foto, status) 
    VALUES (%s,%s,%s,%s,%s,%s,%s)""", (name, surname, email, position, telephone, foto, status))
    conn.commit()

    # сразу находим новое id файла
    cur.execute('SELECT id FROM employee WHERE surname = %s', (surname,))
    id_data = cur.fetchall()
    conn.commit()
    for items in id_data:
        for item in items:
            id_final = item

    foto_final = 'static/images/foto/' + f'{id_final}_' + f'{surname}.jpg'
    #меняем и имя файла в папке
    os.rename(f'static/images/foto/{surname}.jpg', f'static/images/foto/{id_final}_{surname}.jpg')
    # меняем название картинки-фото
    cur.execute("""
    UPDATE employee
    SET foto = %s

    WHERE id = %s
    """, (foto_final, id_final))
    conn.commit()

    return flash('Сотрудник успешно зарегистрирован, EspinosaAlex\n')


def db_delete_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM employee WHERE ID = {0}'.format(id))
    conn.commit()
    return flash('Сотрудник успешно удален')


def db_edit_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM employee WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    article_show = data[0]
    return article_show


def db_final_edit_employee(id, file1):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    position = request.form['position']
    telephone = request.form['telephone']

    if request.form.get('check_false') == 'on':
        status = False
    elif request.form.get('check_true') == 'on':
        status = True

    #меняем и имя файла в папке
    foto = 'static/images/foto/' + f'{id}_' + f'{surname}.jpg'
    #меняем и имя файла в папке
    try:
        # если вдруг у нас уже есть такой, файл, то, чтобы не было конфликта удаляем старое фото и ставим новое
        os.remove(f'static/images/foto/{id}_{surname}.jpg')
        os.rename(f'static/images/foto/{surname}.jpg', f'static/images/foto/{id}_{surname}.jpg')
    except:
        pass


    cur.execute("""
    UPDATE employee
    SET name = %s,
        surname = %s,
        email = %s,
        position = %s,
        telephone = %s,
        foto = %s,
        status = %s

    WHERE id = %s
    """, (name, surname, email, position, telephone, foto, status, id))
    conn.commit()
    return flash(f'Данные сотрудника успешно изменены, {surname} {name}\n')



