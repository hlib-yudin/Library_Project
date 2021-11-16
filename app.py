from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, request, redirect, json, session as flask_session
from config import Config
from datetime import date
import json


app = Flask(__name__, template_folder='boostrap/Pages')
# app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/library_db"
app.config['SECRET_KEY'] = 'Never-Gonna-Give-You-Up__Never-Gonna-Let-You-Down'
#SQLALCHEMY_TRACK_MODIFICATIONS = 'False'

db = SQLAlchemy(app)
db.init_app(app)

from models import *


"""@app.route('/')
def hello_world():
    return 'Hello World!'"""


# змініть цей URL, будь ласка
@app.route("/books/return/submit", methods = ('POST',))
def return_books():
    # Функція для повернення книг (ще не зроблена)
    print(request.form.getlist("book_ids"))
    arrived_json = request.data.decode('utf-8')
    # data -- готовий список словників, з яким можна працювати
    data = json.loads(arrived_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    return 'ok'



@app.route("/books/return", methods = ('GET', 'POST'))
def page_for_returning_books():
    # Рендерить сторінку для підтвердження повернення книги.
    json_orders = {}

    # якщо в поле вводу ввели логін користувача -- знайти і відобразити всі його замовлення
    if request.args.get("login_query"): # and request.method == 'GET'
        # TODO: exceptions
        login_query = request.args["login_query"]
        users = UserInf.query.filter_by(user_login=login_query).all()
        if len(users) != 1:
            # TODO: що повертає при помилці?
            return "user not found"
        user = users[0]
        orders = Order.query.filter_by(user_id=user.user_id, is_canceled=False).all()
        # TODO: що повертає при відсутності замовлень?
        if len(orders) == 0:
            return "no orders"

        # складаємо json з інформацією про замовлення
        json_orders = {"user_id": user.user_id, "orders": []}
        for order in orders:
            books = OrderBook.query.filter_by(order_id=order.order_id).all()
            books = [book.book for book in books if book.return_date == None]
            new_json = {
                "order_id": order.order_id,
                "order_issue_date": order.issue_date,
                "order_in_time": True, # TODO: обчислити, чи минув термін здачі замовлення, чи ні
                "books": []
            }
            for book in books:
                edition = book.edition
                new_json_2 = {
                    "book_id": book.book_id,
                    "edition_name": edition.book_title,
                    "edition_authors": [author.author_surname + " " +  author.author_name + " " + 
                        (author.author_middle_name if author.author_middle_name else "")
                        for author in edition.authors],
                    "edition_year": edition.edition_year
                }
                new_json["books"].append(new_json_2)

            json_orders["orders"].append(new_json)


    # відобразити html-сторінку
    """json_orders = {
        "user_id": "",
        "orders": [{
            "order_id": "1",
            "order_issue_date": "20-08-20",
            "order_in_time": True,
            "books": [{
                "book_id": "333-888-000",
                "edition_name": "Harry Potter",
                "edition_authors": ["JK", "Rowling"],
                "edition_year": 2007,
            },
            {
                "book_id": "333-888-001",
                "edition_name": "Harry Potter 2",
                "edition_authors": ["J.K. Rowling"],
                "edition_year": 2008,
            }]
                
        }]
    }"""
    return render_template('returnBooks.html', json = json_orders)


@app.route('/')
def index():
    #a = take_books_data()
    #print(check_availability(['5-325-00380-1']))
    #print(sign_up("7", "7777", "Гліб", "Юдін", None, "reader"))
    #print(db.session.query(t_user_role).filter_by(role_id = 2).all())
    #print(log_in("6", "7776"))
    #print(log_in("6", "6666"))
    return redirect(url_for("page_for_returning_books"))
    #return 'ok'


def take_books_data():
    book_data_list = []
    editions = EditionInf.query.all()
    for edition in editions:
        edition_genres = edition.genres
        edition_genres = ", ".join(genre.genre for genre in edition_genres)

        edition_authors = edition.authors
        edition_authors = ", ".join(" ".join([author.author_name, str(author.author_middle_name or ''), author.author_surname]) for author in edition_authors)
        num_of_available = EditionCount.query.filter_by(edition_id=edition.edition_id).all()[0]
        book_data_output = {
            "edition_id": edition.edition_id,
            "book_title": edition.book_title,
            "authors": edition_authors,
            "genres": edition_genres,
            "year": edition.edition_year,
            "number_of_available": num_of_available.number_of_available
        }
        book_data_list.append(book_data_output)
        print(book_data_output)
    return book_data_list


def find_by_title(title):
    book_data_list = []
    editions = EditionInf.query.filter_by(book_title=title).all()
    for edition in editions:
        edition_genres = edition.genres
        edition_genres = ", ".join(genre.genre for genre in edition_genres)

        edition_authors = edition.authors
        edition_authors = ", ".join(" ".join([author.author_name, str(author.author_middle_name or ''), author.author_surname]) for author in edition_authors)

        book_data_output = {
            "edition_id": edition.edition_id,
            "book_title": edition.book_title,
            "authors": edition_authors,
            "genres": edition_genres,
            "year": edition.edition_year
        }
        book_data_list.append(book_data_output)
        print(book_data_output)
    return book_data_list


def check_availability(editions_id):
    check_list = []
    res_flag = 0
    for edition_id in editions_id:
        edition = EditionCount.query.filter_by(edition_id=edition_id).all()[0]
        flag = edition.number_of_available > 0
        if flag == False:
            res_flag = 1
        check_list.append({"edition_id": edition.edition_id, "flag": flag})
    if res_flag == 0:
        return 'ok ok'
    else:
        return check_list


def sign_up(login, password, first_name, last_name, middle_name, role_name):
    # Проводить реєстрацію користувача з даними полями.
    # Логін і пароль приходять вже в зашифрованому вигляді (sha-256).

    # шукаємо користувачів з даним логіном
    users = UserInf.query.filter_by(user_login = login).all()
    # якщо вони вже існують -- не проводимо реєстрацію
    if len(users) > 0:
        # TODO: замість тексту повернути json
        return "Даний логін вже існує"
    else:
        # створити нового користувача
        new_user = UserInf(user_login = login,
                           user_password = password,
                           user_name = first_name,
                           surname = last_name,
                           middle_name = middle_name)
        # додати його в таблицю UserInf
        db.session.add(new_user)
        # додати його роль в таблицю t_user_role
        added_user = UserInf.query.filter_by(user_login = login, user_password = password).first()
        role = Role.query.filter_by(role_name = role_name).first()
        added_user.role = role
        # додати його статус в таблицю t_user_status
        status = Status.query.filter_by(status_name = "normal").first()
        added_user.status = status
        # зберегти зміни -- TODO, після того, як перевірено правильність роботи цієї функції
        print(added_user)
        db.session.commit()
        return "sign_up -- ok"


def log_in(login, password):
    # Проводить авторизацію користувача з вказаними зашифрованими логіном і паролем.
    users = UserInf.query.filter_by(user_login = login, user_password = password).all()
    if len(users) == 0:
        # TODO: замінити текст на json
        return "Неправильний логін чи пароль"
    else:
        # зберегти інформацію про користувача в сесію
        user = users[0]
        flask_session['id'] = user.user_id
        flask_session['name'] = user.user_name
        flask_session['role'] = user.role.role_name
        print(user, user.role.role_name)
        return "log_in - ok"








if __name__ == '__main__':
    app.run(debug=True)
