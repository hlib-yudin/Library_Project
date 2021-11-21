from flask_sqlalchemy import SQLAlchemy
from flask import Flask, make_response, render_template, url_for, request, redirect, jsonify,json, flash, session
from flask_session import Session  # https://pythonhosted.org/Flask-Session
from config import Config
from datetime import date
from dateutil.relativedelta import *
import json

app = Flask(__name__, template_folder='boostrap/Pages')
# app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1111@localhost:5432/postgres"

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/library_db"
app.config['SECRET_KEY'] = 'Never-Gonna-Give-You-Up__Never-Gonna-Let-You-Down'

# SQLALCHEMY_TRACK_MODIFICATIONS = 'False'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # So the token cache will be stored in a server-side session
Session(app)

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

@app.route('/orders')
def page_for_orders():
    # Сторінка для відображення замовлень користувача (її бачить не бібліотекарЮ, а читач)
    if not session.get('id'):
        return "Авторизуйтеся"
    user_id = session["id"]
    user = UserInf.query.filter_by(user_id=user_id).first()
    # показуємо лише заброньовані та не повністю повернені замовлення
    # TODO: не показувати повністю повернені замовлення!!!!!!!!!!!!!!!!!!!!!!!!
    orders = Order.query.filter_by(user_id=user_id, is_canceled=False).all()

    # складаємо json з інформацією про замовлення
    json_orders = {"user_id": user.user_id, "orders": []}
    for order in orders:
        books = OrderBook.query.filter_by(order_id=order.order_id).all()
        books = [book.book for book in books if book.return_date == None]
        new_json = {
            "order_id": order.order_id,
            "order_status": "Видане" if order.issue_date else "Заброньоване",
            #"order_issue_date": order.issue_date,
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

        if len(new_json['books']) > 0:
            json_orders["orders"].append(new_json)

    if len(json_orders['orders']) == 0:
        return "Замовлень немає"
    return render_template('viewOrders.html', json = json_orders)

@app.route("/books/catalogue")
def catalogue():
    return render_template('catalog.html')

@app.route("/books/basket")
def basket():
    return render_template('basket.html')

@app.route("/books/signin")
def signin():
    return render_template('signin.html')

@app.route("/books/issuingBook")
def issuebooks():
    return render_template('issuingBook.html')

@app.route("/books/signup")
def signup():
    return render_template('signup.html')

@app.route("/books/addBook")
def addBook():
    return render_template('addBook.html')

@app.route("/books/removeBook")
def removeBook():
    return render_template('removeBook.html')

@app.route("/books/orders")
def viewOrders():
    return render_template('viewOrders.html')

@app.route("/scripts/navbarCreation")
def navbarCretionScript():
    return render_template('navbarCreation.js')

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

    is_dep = is_debtor(user_id)
    if old_user_status == 'debtor' and not is_debtor(user_id):
        change_user_status(user_id, 'normal')
    if old_user_status != 'debtor' and all_books_returned(user_id):
        grant_privileges(user_id)

    for el in res:
        print(el)
    # db.session.commit()
    return make_response(jsonify({'message': "Книги успішно повернено"}))



@app.route("/order/issue", methods=('POST',))
def issue_order():
    # Функція для підтвердження видачі замовлення.
    # Приймає json: {"user_login": ...,    "order_id": ... }
    # TODO: нормально протестувати цю функцію!!!!!

    arrived_json = json.loads(request.data.decode('utf-8'))
    # arrived_json = {"user_login": '3', "order_id": 1}
    print(arrived_json)
    arrived_login = arrived_json["user_login"]
    arrived_order_id = arrived_json["order_id"]

    order_u_login = db.session.query(Order.order_id, UserInf.user_login, Order.is_canceled).filter(
        Order.order_id == arrived_order_id,
        Order.user_id == UserInf.user_id).first()
    # 1) валідація
    # чи є такий логін?
    users = UserInf.query.filter_by(user_login=arrived_login).all()
    if len(users) == 0:
        return make_response(jsonify({'res_message': 'no users with given login!'}))
    # чи є таке замовлення?
    user = users[0]
    orders = Order.query.filter_by(order_id=arrived_order_id).all()
    if len(orders) == 0:
        return make_response(jsonify({'res_message': 'no orders with given id!'}))

    # чи має даний юзер дане замовлення?
    order = orders[0]
    if order_u_login.user_login != arrived_login:
        return make_response(jsonify({'res_message': "given person didn't make given order!"}))

    # чи скасоване замовлення?
    if order.is_canceled:
        return make_response(jsonify({'res_message': 'order was canceled!'}))

    # чи замовлення вже видане?
    if order.issue_date:
        return make_response(jsonify({'res_message': 'order was already issued!'}))

    # чи є читач боржником?
    if user.status.status_name == 'debtor':
        # якщо боржник -- скасувати замовлення
        order.is_canceled = True
        # db.session.commit()

        return make_response(jsonify({'res_message': 'person is debtor -- order was cancelled!'}))

    # якщо читач є боржником, але в базі даних про це ще немає інформації
    if is_debtor(user.user_id):
        order.is_canceled = True
        user.status = Status.query.filter_by(status_name='debtor').first()
        # db.session.commit()
        return make_response(jsonify({'res_message': 'person is debtor -- order was cancelled!'}))

    # 2) оновити запис в БД: таблиця Orders -- оновити issue_date
    order.issue_date = date.today().strftime('%Y-%m-%d')
    print(order.issue_date)
    # db.session.commit()
    return make_response(jsonify({'res_message': 'order was successfully issued!'}))



@app.route("/books/return", methods = ('GET', 'POST'))
def page_for_returning_books():
    # Рендерить сторінку для підтвердження повернення книги.
    json_orders = {'user_id': '', 'orders':[], 'error_message': ''}

    # якщо в поле вводу ввели логін користувача -- знайти і відобразити всі його замовлення
    if request.args.get("login_query"):  # and request.method == 'GET'
        # TODO: exceptions
        login_query = request.args["login_query"]
        users = UserInf.query.filter_by(user_login=login_query).all()
        if len(users) != 1:
            # TODO: що повертає при помилці?
            #return make_response(jsonify({'message': 'Користувача не знайдено!'}))
            json_orders['error_message'] = 'Користувача не знайдено!'
            return render_template('returnBooks.html', json=json_orders)
        user = users[0]
        orders = Order.query.filter(Order.user_id==user.user_id, Order.is_canceled==False,
            Order.issue_date != None).all()
        # TODO: що повертає при відсутності замовлень?
        # повернемо json, у якого 'orders' = []
        if len(orders) == 0:
            #return make_response(jsonify({'message': 'Замовлення не знайдено!'}))
            json_orders['error_message'] = 'Для даного користувача замовлень не знайдено!'
            return render_template('returnBooks.html', json=json_orders)

        # складаємо json з інформацією про замовлення
        json_orders = {"user_id": user.user_id, "orders": [], 'error_message': ''}
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

            if len(new_json['books']) > 0:
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
        #db.session.commit()
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
                                                                                            Order.is_canceled != False,
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



# --------------------------Герасимчук -- Кошик та оформлення замовлення---------------------------------------------
# функція працює коректно при умові, що return_date = None
def is_canceled_change(ord):
    allowed_booking_days = 14
    # треба перевірити скільки бронь вже висить
    today_date = date.today()
    order_date = ord.booking_date
    booking_days = number_of_days(order_date, today_date)
    if allowed_booking_days < booking_days:
        # is_canceled is True
        ord.is_canceled_update(new_status=True)
        return 1
    return 0


def ordered_books_check(books):
    new_book_list = list()
    for inf in books:
        book_id = inf.book_id
        issue_date = inf.issue_date
        if issue_date is None and is_canceled_change(inf):
            continue
        else:
            new_book_list.append(book_id)
    return new_book_list


def available_books_now(edition_id):
    # список всіх книжок одного видання
    edition_books = db.session.query(Book.book_id).filter_by(edition_id=edition_id).all()

    # книжки одного видання, яких немає в наявності, тому що заброньовані, або не повернені
    ordered_books = db.session.query(Book.book_id, Order.booking_date, Order.issue_date).\
        join(OrderBook, Book.book_id == OrderBook.book_id).\
        join(Order, Order.order_id == OrderBook.order_id). \
        filter(Book.edition_id == edition_id, OrderBook.return_date == None, Order.is_canceled == False).all()
    # перевірка коректності списку книг ordered_books
    checked = ordered_books_check(ordered_books)

    edition_books_list = list()
    for el in edition_books:
        edition_books_list.append(el[0])

    A = set(edition_books_list)
    B = set(checked)
    books = list(A.difference(B))
    return books


def can_add(user_id):
    amount_of_books = {'normal': 10, 'privileged': 10, 'debtor': 0}
    order_list = db.session.query(Order.order_id).filter_by(user_id=user_id).all()
    user_status = UserInf.query.filter_by(user_id=user_id).first().status.status_name
    in_hands = 0
    for order in order_list:
        return_date = db.session.query(OrderBook.return_date).filter_by(order_id=order.order_id).all()
        for re_date in return_date:
            if re_date.return_date is None:
                in_hands += 1
    if amount_of_books[user_status] > in_hands:
        can_add = amount_of_books[user_status] - in_hands
        return can_add
    else:
        return 0


def order(user_id, chosen_books):
    # створити новий запис в бд в Orders
    order_id = Order.add(user_id=user_id)
    for edition_id in chosen_books:
        edition_amount = db.session.query(EditionCount).filter_by(edition_id=edition_id).first().number_of_available
        if edition_amount > 0:
            # edition_amount need to be equal to len(available_books)
            available_books = available_books_now(edition_id)
            b_order_id = available_books[-1]
            # створити новий запис в бд в Order_book
            OrderBook.add(book_id=b_order_id, order_id=order_id.order_id)
            # після бронювання книги зменшуємо кількість однакових книг
            book = db.session.query(EditionCount).filter_by(edition_id=edition_id).first()
            book.count_update()
        else:
            return "книги немає в наявності"
    return "замовлення пройшло успішно"


# Після натиснення на кнопку addBook, зберігає edition_id в сесію,
# якщо обрали більше чим 1 книгу, буде список з edition_id
# треба цей edition_book_user_dict для наступної функції
@app.route("/books/catalogue/addBook", methods=['POST'])
def add_book_to_basket():
    session.modified = True  # для того, щоб сесія оновлювалась
    # мені можна посилати лише edition_id, адже user_id привязаний до сесії
    data = json.loads(request.data);
    edition_id = data['edition_id']
    if session.get('id'):
        session['basket'].append(edition_id)
    return make_response(jsonify({'response':'book added'}))


@app.route("/books/basket/data", methods=['GET'])
def basket_data():
    user_id = session['id']
    chosen_books = session['basket']
    main_json = {'user_id': user_id, 'basket': []}
    for book_edition_id in chosen_books:
        book_info = db.session.query(EditionInf).filter_by(edition_id=book_edition_id).first()
        book_title = book_info.book_title
        edition_year = book_info.edition_year
        basket_json = {'edition_id': book_edition_id,
                       'book_title': book_title,
                       'edition_year': edition_year}
        main_json['basket'].append(basket_json)
    print(main_json)
    return make_response(jsonify(main_json))


# приймається список книг(edition_id), які користувач вирішив видалити
@app.route("/books/basket/delete", methods=['POST'])
def book_ordering_amount():
    data = json.loads(request.data);
    edition_id = data['edition_id']
    if session.get('id'):
        session['basket'].remove(edition_id)
    return make_response(jsonify({'response':'book deleted'}))


@app.route("/books/basket/submit", methods=['GET'])
def order_submit():
    # chosen_books - все, що додано до кошика
    chosen_books = session['basket']
    user_id = session['id']
    amount_of_chosen = len(chosen_books)
    books_can_add = can_add(user_id)
    need_to_delete = amount_of_chosen - books_can_add
    if books_can_add == 0:
        return make_response(jsonify({'response':"User can not order because is debtor or already have 10 books"}))
    elif need_to_delete > 0:
        # зробити з цього один ретурн - повідомлення
        print("Кількість книг, які треба видалити ", need_to_delete)
        return 1
    order(user_id, chosen_books)
    session['basket'].clear()
    return make_response(jsonify({'response': "Order complete"}))
# -------------------------------------------------------------------------------------------------------------------


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

@app.route("/catalogue/search", methods = ['POST'])
def find_by_title():
    title_json = request.data.decode('utf-8')
    title = json.loads(title_json)['input']
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
    return  make_response(jsonify({'books':book_data_list}))


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
    """print(request.data)
    arrived_json = json.loads(request.data.decode('utf-8'))
    login = arrived_json["user_login"]
    password = arrived_json["user_password"]
    first_name = arrived_json["user_name"]
    last_name = arrived_json["surname"]
    middle_name = arrived_json["middle_name"]"""
    login = request.form["user_login"]
    password = request.form["user_password"]
    first_name = request.form["user_name"]
    last_name = request.form["surname"]
    middle_name = request.form["middle_name"]

    # шукаємо користувачів з даним логіном
    users = UserInf.query.filter_by(user_login=login).all()
    # якщо вони вже існують -- не проводимо реєстрацію
    if len(users) > 0:
        flash("Даний логін вже існує!")
        return redirect(url_for('signup'))

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
        # поки додаємо лише читачів -- TODO: додавати бібліотекарів теж
        role_name = 'reader'
        role = Role.query.filter_by(role_name=role_name).first()
        added_user.role = role

        # додати його статус в таблицю t_user_status
        status = Status.query.filter_by(status_name="normal").first()
        added_user.status = status
        # зберегти зміни
        print(added_user)
        db.session.commit()
        
        users = UserInf.query.filter_by(user_login=login, user_password=password).all()
        # зберегти інформацію про користувача в сесію
        user = users[0]
        session['id'] = user.user_id
        session['name'] = user.user_name
        session['role'] = user.role.role_name
        session['basket'] = []
        session['permissions'] = []
        role_permission = db.session.query(t_role_permission).filter_by(role_id=user.role.role_id).all()
        permission_ids = [elem[1] for elem in role_permission]
        for perm_id in permission_ids:
            perm = Permission.query.filter_by(permission_id=perm_id).first()
            session['permissions'].append(perm.permission_description)
    if user.role.role_name == 'librarian': 
        return redirect("/books/return")
    else:
        return redirect(url_for('catalogue'))

@app.route("/role/user", methods = ['GET'])
def getUserRole():
    return make_response(jsonify({'role': session['role'], 'permissions': session['permissions']}))


@app.route("/login/user", methods = ['POST'])
def log_in():
    print(request.form)
    permission_for_page = {
        'add books':'addBook',
        'delete books': 'issuebooks',
        'issue/accept books':'issuebooks',
        'order books':'/orders',
        'register librarians':'',
    }
    #arrived_json = json.loads(request.data.decode('utf-8'))
    #login = arrived_json["user_login"]
    #password = arrived_json["user_password"]
    login = request.form["user_login"]
    password = request.form["user_password"]
    print(login)
    # Проводить авторизацію користувача з вказаними зашифрованими логіном і паролем.
    users = UserInf.query.filter_by(user_login=login, user_password=password).all()
    if len(users) == 0:
        flash("Неправильний логін чи пароль!")
        return redirect(url_for('signin'))

    else:
        # зберегти інформацію про користувача в сесію
        user = users[0]
        session['id'] = user.user_id
        session['name'] = user.user_name
        session['role'] = user.role.role_name
        session['basket'] = []
        session['permissions'] = []
        print(session)

        role_permission = db.session.query(t_role_permission).filter_by(role_id = user.role.role_id).all()
        permission_ids = [elem[1] for elem in role_permission]
        for perm_id in permission_ids:
            perm = Permission.query.filter_by(permission_id=perm_id).first()
            session['permissions'].append(perm.permission_description)

    role = user.role.role_name
    print(session['permissions'])
    #return "log_in - ok"
    if user.role.role_name == 'librarian': 
        return redirect("/books/return")
    else:
        return redirect(url_for('catalogue'))


if __name__ == '__main__':
    app.run(debug=True)
