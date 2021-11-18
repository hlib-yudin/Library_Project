from flask_sqlalchemy import SQLAlchemy
from flask import Flask, make_response, render_template, url_for, request, redirect, jsonify,json, session as flask_session
from config import Config
from datetime import date
from dateutil.relativedelta import *
import json

app = Flask(__name__, template_folder='boostrap/Pages')
# app.config.from_object(Config)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1111@localhost:5432/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/library_db"
app.config['SECRET_KEY'] = 'Never-Gonna-Give-You-Up__Never-Gonna-Let-You-Down'
# SQLALCHEMY_TRACK_MODIFICATIONS = 'False'

db = SQLAlchemy(app)
db.init_app(app)

from models import *

"""@app.route('/')
def hello_world():
    return 'Hello World!'"""

# html routing
@app.route('/')
def index():

    #return redirect(url_for("page_for_returning_books"))
    return redirect(url_for('signup'))

@app.route("/books/catalogue")
def catalogue():
    return render_template('catalog.html')

@app.route("/books/basket")
def basket():
    return render_template('basket.html')

@app.route("/books/signin")
def sigin():
    return render_template('signin.html')

@app.route("/books/signup")
def signup():
    return render_template('signup.html')

@app.route("/books/addBook")
def addBook():
    return render_template('addBook.html')

@app.route("/books/removeBook")
def removeBook():
    return render_template('removeBook.html')

@app.route("/scripts/navbarCreation")
def navbarCretionScript():
    return render_template('navbarCreation.js')

@app.route("/navbar/css")
def signincss():
    return render_template('sign.css')

@app.route("/style/css")
def stylecss():
    return render_template('style.css')

@app.route("/shopping/css")
def shoppingcss():
    return render_template('shopping.css')

@app.route("/books/return/submit", methods = ('POST',))
def return_books():
    # Функція для повернення книг (ще не зроблена)
    #print(request.form.getlist("book_ids"))
    arrived_json = request.data.decode('utf-8')
    # data -- готовий список словників, з яким можна працювати
    data = json.loads(arrived_json)
    print(data)
    print('-------------------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------------------')

    if len(data) == 0:
        print('Читач повернув усі книжки')
        return 'Читач повернув усі книжки'
    # s = json.dumps(data, indent=4, sort_keys=True)
    user_id = data[0]['user_id']
    old_user_status = get_user_status(user_id)
    res = return_of_book(data)
    db.session.commit()
    is_dep = is_debtor(user_id)
    if old_user_status == 'debtor' and not is_debtor(user_id):
        change_user_status(user_id, 'normal')
    if old_user_status != 'debtor' and all_books_returned(user_id):
        grant_privileges(user_id)

    for el in res:
        print(el)
    # db.session.commit()
    return 'ok'



@app.route('/order/issue')
def issue_order():
    # Функція для підтвердження видачі замовлення.
    # Приймає json: {"user_login": ...,    "order_id": ... }
    # TODO: нормально протестувати цю функцію!!!!!

    #arrived_json = json.loads(request.data.decode('utf-8'))
    arrived_json = {"user_login": '3', "order_id": 1}
    print(arrived_json)
    arrived_login = arrived_json["user_login"]
    arrived_order_id = arrived_json["order_id"]

    # 1) валідація 
    # чи є такий логін?
    users = UserInf.query.filter_by(user_login = arrived_login).all()
    if len(users) == 0:
        return "no users with given login"

    # чи є таке замовлення?
    user = users[0]
    orders = Order.query.filter_by(order_id = arrived_order_id).all()
    if len(orders) == 0:
        return "no orders with given id"

    # чи має даний юзер дане замовлення?
    order = orders[0]
    if order.user.user_id != user.user_id:
        return "given person didn't make given order"

    # чи скасоване замовлення?
    if order.is_canceled:
        return "order was canceled"

    # чи замовлення вже видане?
    if order.issue_date:
        return "order was already issued"

    # чи є читач боржником?
    if user.status.status_name == "debtor":
        # якщо боржник -- скасувати замовлення
        order.is_canceled = True
        #db.session.commit()
        return "person is debtor -- order was cancelled" 

    # якщо читач є боржником, але в базі даних про це ще немає інформації
    if is_debtor(user.user_id):
        order.is_canceled = True
        user.status = Status.query.filter_by(status_name = "debtor").first()
        #db.session.commit()
        return "person is debtor -- order was cancelled" 


    # 2) оновити запис в БД: таблиця Orders -- оновити issue_date
    order.issue_date = date.today().strftime('%Y-%m-%d')
    print(order.issue_date)
    #db.session.commit()
    return "order was successfully issued"




@app.route("/books/return", methods = ('GET', 'POST'))
def page_for_returning_books():
    # Рендерить сторінку для підтвердження повернення книги.
    json_orders = {}

    # якщо в поле вводу ввели логін користувача -- знайти і відобразити всі його замовлення
    if request.args.get("login_query"):  # and request.method == 'GET'
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
                "order_in_time": True,  # TODO: обчислити, чи минув термін здачі замовлення, чи ні
                "books": []
            }
            for book in books:
                edition = book.edition
                new_json_2 = {
                    "book_id": book.book_id,
                    "edition_name": edition.book_title,
                    "edition_authors": [author.author_surname + " " + author.author_name + " " +
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
    return render_template('returnBooks.html', json=json_orders)



def return_of_book(dict_list):
    # user_status = UserInf.query.filter_by(user_id=user_id).first().status
    # issue_date = Order.query.filter_by(user_id=user_id).all()[0].issue_date
    res_list = []
    for elem in dict_list:
        # elem = json.loads(elem)
        order_id = elem['order_id']
        book_id = elem['book_id']
        edition = Book.query.filter_by(book_id=book_id).first().edition
        edition_id = edition.edition_id
        if OrderBook.query.filter_by(order_id=order_id, book_id=book_id).first().return_date != None:
            res_list.append({"order_id": order_id, "edition_id": edition_id, "book_title": edition.book_title,
                             "message": "Цю книгу вже повернули"})
            continue
        num_rows_updated = OrderBook.query.filter_by(order_id=order_id, book_id=book_id).update(
            dict(return_date=date.today()))

        edition = EditionCount.query.filter_by(edition_id=edition_id).first()
        edition.number_of_available += 1
        res_list.append({"order_id": order_id, "edition_id": edition_id, "book_title": edition.book_title,
                         "message": "Книгу успішно повернуто"})


        print('order_id: {},  edition_id: {}, book_id: {} '.format(order_id, edition_id, book_id))
        print('Current EditionCount:', edition.number_of_available)
        print('Return_date:', OrderBook.query.filter_by(order_id=order_id, book_id=book_id).first().return_date)
        print('-----------------------------------------------------')
        # TODO: додати db.session.commit()
        # db.session.commit()
    return res_list

def get_user_status(user_id):
    return UserInf.query.filter_by(user_id=user_id).first().status.status_name


def change_user_status(user_id, new_status_name):
    new_status_id = Status.query.filter_by(status_name=new_status_name).first().status_id
    if new_status_id == None:
        return 'Такого статуса немає!'
    a = db.session.query(t_user_status).filter(t_user_status.c.user_id == user_id).update(dict(status_id=new_status_id))
    # TODO: додати db.session.commit()

    # TODO: потім видалити наступні рядки
    b = db.session.query(t_user_status).filter(t_user_status.c.user_id == user_id).first()
    print('new_status_id:', b.status_id)


def grant_privileges(user_id):

    subq = db.session.query(Order.order_id,
                           func.max(OrderBook.return_date).label('max_return_date')).filter(Order.user_id == user_id,
                                                                                            Order.order_id == OrderBook.order_id).group_by(
        Order.order_id).subquery('subq')
    res2 = db.session.query(subq.c.order_id, Order.issue_date, subq.c.max_return_date).filter(subq.c.order_id == Order.order_id).order_by(subq.c.max_return_date.desc()).limit(2).all()
    for el in res2:
        # print(el.order_id, el.issue_date, el.book_id, el.max_return_date)
        print(el.order_id, el.issue_date, el.max_return_date)

    term = {'normal': 3, 'privileged': 6}
    user = UserInf.query.filter_by(user_id=user_id).first().status
    num_of_months = term[user.status_name]
    if all([number_of_months(el.issue_date, el.max_return_date) < num_of_months for el in res2]):
        change_user_status(user_id, 'privileged')

    # TODO: додати db.session.commit()
    return 'ok'

def all_books_returned(user_id):

    user_books = db.session.query(OrderBook.book_id, OrderBook.return_date,).filter(Order.user_id == user_id,
                                                                                      Order.order_id == OrderBook.order_id,
                                                                                    OrderBook.return_date == None).first()
    print(user_books)
    if user_books == None:
        return True
    else:
        return False

def number_of_months(date1, date2):
    # if date2 is None:
    #     date2 = date.today()
    months = abs((date1.year - date2.year) * 12 + date1.month - date2.month)
    return months

def number_of_days(date1, date2):
    return abs((date1 - date2).days)

def is_debtor(user_id):
    term = {'normal': 3, 'privileged': 6, 'debtor': 0}
    user_status = UserInf.query.filter_by(user_id=user_id).first().status.status_name
    num_of_months = term[user_status]
    is_debtor_flag = False
    verification_date = date.today() - relativedelta(months=num_of_months)
    user_books = db.session.query(func.count(OrderBook.order_id).label("count")).filter(Order.user_id == user_id,
                                                                                         Order.order_id == OrderBook.order_id,
                                                                                         OrderBook.return_date == None,
                                                                                         Order.issue_date != None,
                                                                                    Order.issue_date < verification_date).first()
    if user_books.count > 0:
        is_debtor_flag = True
    return is_debtor_flag

@app.route("/catalogue/addBook", methods = ['POST'])
def addCatalogueBook():
    book = request.data;
    return render_template('basket.html', json = request.data)

@app.route("/catalogue/return", methods = ['GET'])
def take_books_data():
    if request.method == 'GET':
        book_data_list = []
        editions = EditionInf.query.all()
        for edition in editions:
            edition_genres = edition.genres
            edition_genres = ", ".join(genre.genre for genre in edition_genres)

            edition_authors = edition.authors
            edition_authors = ", ".join(
                " ".join([author.author_name, str(author.author_middle_name or ''), author.author_surname]) for author in
                edition_authors)
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
        #print(book_data_output)
        return make_response(jsonify({'books':book_data_list}))


def find_by_title(title):
    book_data_list = []
    editions = EditionInf.query.filter_by(book_title=title).all()
    for edition in editions:
        edition_genres = edition.genres
        edition_genres = ", ".join(genre.genre for genre in edition_genres)

        edition_authors = edition.authors
        edition_authors = ", ".join(
            " ".join([author.author_name, str(author.author_middle_name or ''), author.author_surname]) for author in
            edition_authors)

        book_data_output = {
            "edition_id": edition.edition_id,
            "book_title": edition.book_title,
            "authors": edition_authors,
            "genres": edition_genres,
            "year": edition.edition_year
        }
        book_data_list.append(book_data_output)
        print(book_data_output)
    return {'res':book_data_list}


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


@app.route('/signup/user', methods = ['POST'])
def sign_up():
    # Проводить реєстрацію користувача з даними полями.
    # Логін і пароль приходять вже в зашифрованому вигляді (sha-256).
    print(request.data);
    '''
    # шукаємо користувачів з даним логіном
    users = UserInf.query.filter_by(user_login=login).all()
    # якщо вони вже існують -- не проводимо реєстрацію
    if len(users) > 0:
        # TODO: замість тексту повернути json
        return "Даний логін вже існує"
    else:
        # створити нового користувача
        new_user = UserInf(user_login=login,
                           user_password=password,
                           user_name=first_name,
                           surname=last_name,
                           middle_name=middle_name)
        # додати його в таблицю UserInf
        db.session.add(new_user)
        # додати його роль в таблицю t_user_role
        added_user = UserInf.query.filter_by(user_login=login, user_password=password).first()
        role = Role.query.filter_by(role_name=role_name).first()
        added_user.role = role
        # додати його статус в таблицю t_user_status
        status = Status.query.filter_by(status_name="normal").first()
        added_user.status = status
        # зберегти зміни -- TODO, після того, як перевірено правильність роботи цієї функції
        print(added_user)
        db.session.commit()
    '''
    return "sign_up -- ok"

@app.route("/login/user", methods = ['POST'])
def log_in():
    print(request.data)
    arrived_json = json.loads(request.data.decode('utf-8'))
    login = arrived_json["user_login"]
    password = arrived_json["user_password"]
    # Проводить авторизацію користувача з вказаними зашифрованими логіном і паролем.
    users = UserInf.query.filter_by(user_login=login, user_password=password).all()
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
