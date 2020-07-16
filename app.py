# -*- coding: utf-8 -*-
from flask import Flask, flash, render_template, redirect, request, \
    make_response
import datetime
from modules import parser


app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    '''Основная функция, которая обрабатывает запрос и рендерит страницу'''
    status = request.cookies.get('status')
    if not status:
        return render_template('login.html')
    elif status == 'Bad Login':
        response = make_response(render_template('login.html', bad_login=True))
        response.set_cookie('status', '0', max_age=0)
        return response
    elif status == 'Bad Login Main Page':
        diary = request.cookies.get('diary')
        update_date = request.cookies.get('update_date')
        response = make_response(
            render_template(
                'main.html', bad_login=True,
                diary=eval(diary), update_date=update_date
            )
        )
        response.set_cookie('status', 'Good', max_age=60*60*24*7)
        return response
    elif status == 'Good':
        diary = request.cookies.get('diary')
        update_date = request.cookies.get('update_date')
        response = make_response(
            render_template(
                'main.html', diary=eval(diary),
                update_date=update_date
            )
        )
        response.set_cookie('status', 'Good', max_age=60*60*24*7)
        return response


@app.route('/login', methods=['POST'])
def login():
    '''Фунция для получения страницы с отметками'''
    login = request.form['login']
    password = request.form['password']

    diary = parser.fill_diary(login, password)
    response = make_response(redirect('/'))

    if diary == 'Bad Login':
        response.set_cookie('status', 'Bad Login', max_age=60*60*24*7)
        return response
    else:
        response.set_cookie('status', 'Good', max_age=60*60*24*7)
        response.set_cookie('login', login, max_age=60*60*24*7)
        response.set_cookie('diary', str(diary), max_age=60*60*24*7)
        response.set_cookie(
            'update_date',
            '{0:%d.%m.%Y} в {0:%H:%M}'.format(datetime.datetime.now()),
            max_age=60*60*24*7
        )
        return response


@app.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('status', '0', max_age=0)
    return response


@app.route('/update', methods=['POST'])
def update():
    '''Функция обновляет отметки пользователя'''
    login = request.cookies.get('login')
    password = request.form['password']

    diary = parser.fill_diary(login, password)
    response = make_response(redirect('/'))

    if diary == 'Bad Login':
        response.set_cookie('status', 'Bad Login Main Page', max_age=60*60*24*7)
        return response
    else:
        response.set_cookie('status', 'Good', max_age=60*60*24*7)
        response.set_cookie('diary', str(diary), max_age=60*60*24*7)
        response.set_cookie(
            'update_date',
            '{0:%d.%m.%Y} в {0:%H:%M}'.format(datetime.datetime.now()),
            max_age=60*60*24*7
        )
        return response
