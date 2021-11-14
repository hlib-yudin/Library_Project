from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, request, redirect, json
from config import Config


app = Flask(__name__)
# app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/postgres"
#SQLALCHEMY_TRACK_MODIFICATIONS = 'False'

db = SQLAlchemy(app)
db.init_app(app)

from models import *


"""@app.route('/')
def hello_world():
    return 'Hello World!'"""

@app.route('/')
def index():
    take_books_data()
    print(check_availability(['5-325-00380-1']))
    #print(sign_up("7", "7777", "Гліб", "Юдін", None, "reader"))
    print(db.session.query(t_user_role).filter_by(role_id = 2).all())
    return 'ok'


def take_books_data():
    book_data_list = []
    editions = EditionInf.query.all()
    for edition in editions:
        edition_genres = edition.genres
        edition_genres = ", ".join(genre.genre for genre in edition_genres)

        edition_authors = edition.authors
        edition_authors = ", ".join(" ".join([author.author_name, str(author.author_middle_name or ''), author.author_surname]) for author in edition_authors)
        num_of_available = EditionInf.query.filter_by(edition_id=edition.edition_id).all()[0]
        book_data_output = {
            "edition_id": edition.edition_id,
            "book_title": edition.book_title,
            "authors": edition_authors,
            "genres": edition_genres,
            "year": edition.edition_year,
            #"number_of_available": num_of_available.number_of_available
            "number_of_available": num_of_available.edition_count.number_of_available
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

    # print(check_availability(['5-325-00380-1', '5-325-00380-11-copy']))

    # for edition in editions:
    #     edition_genres = edition.genres
    #     edition_genres = ", ".join(genre.genre for genre in edition_genres)
    #
    #     edition_authors = edition.authors
    #     edition_authors = ", ".join(" ".join([author.author_name, str(author.author_middle_name or ''), author.author_surname]) for author in edition_authors)
    #
    #     book_data_output = {
    #         "edition_id": edition.edition_id,
    #         "book_title": edition.book_title,
    #         "authors": edition_authors,
    #         "genres": edition_genres,
    #         "year": edition.edition_year
    #     }
    #     book_data_list.append(book_data_output)
    #     print(book_data_output)





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
        return "ok"







if __name__ == '__main__':
    app.run(debug=True)
