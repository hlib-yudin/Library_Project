from graphіcs import *
from datetime import *

# html routing
@app.route('/')
def index():
    session.clear()
    return redirect(url_for('catalogue'))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

@app.route("/books/catalogue")
def catalogue():
    return render_template('catalog.html')


@app.route("/books/basket")
def basket():
    return render_template('basket.html')


@app.route("/login")
def signin():
    return render_template('signin.html')


@app.route("/books/issuingBook")
def issuebooks():
    return render_template('issuingBook.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route("/signup/librarians")
def page_for_registering_librarians():
    return render_template('register_librarians.html')


@app.route("/books/addBook")
def addBook():
    return render_template('addBook.html')


@app.route("/books/removeBook")
def removeBook():
    return render_template('removeBook.html')


@app.route("/librarian/analytics")
def analytics():
    check_graphіc_file()
    return render_template('analytics.html')


@app.route("/scripts/navbarCreation")
def navbarCretionScript():
    return render_template('navbarCreation.js')


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

@app.route("/books/return", methods=('GET', 'POST'))
def page_for_returning_books():
    # Рендерить сторінку для підтвердження повернення книги.
    json_orders = {"user_id": None, "orders": None, 'message': ""}

    # якщо в поле вводу ввели логін користувача -- знайти і відобразити всі його замовлення
    if request.args.get("login_query"):  # and request.method == 'GET'
        # TODO: exceptions
        login_query = request.args["login_query"].strip()
        users = get_all_users_by_login(login_query)
        if len(users) != 1:
            json_orders['message'] = "Користувача не знайдено!"
            return render_template('returnBooks.html', json=json_orders)

        user = users[0]
        orders = get_issued_orders_by_user_id(user.user_id)
        print(orders)
        if len(orders) == 0:
            print("here")
            json_orders['message'] = "Актуальних замовлень не знайдено!"
            return render_template('returnBooks.html', json=json_orders)

        # складаємо json з інформацією про замовлення
        json_orders = {"user_id": user.user_id, "orders": [], 'message': ''}
        for order in orders:
            books = get_all_books_by_order_id(order.order_id)
            books = [book.book for book in books if book.return_date == None]
            new_json = {
                "order_id": order.order_id,
                "order_issue_date": order.issue_date,
                "order_in_time": True,
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
    return render_template('returnBooks.html', json=json_orders)


@app.route("/books/return/submit", methods=('POST',))
def return_books():
    # print(request.form.getlist("book_ids"))
    arrived_json = request.data.decode('utf-8')
    # data -- готовий список словників, з яким можна працювати
    data = json.loads(arrived_json)
    print(data)
    print(
        '-------------------------------------------------------------------------------------------------------------')
    print(
        '-------------------------------------------------------------------------------------------------------------')

    if len(data) == 0:
        return make_response(jsonify({'message': "Не обрано жодної книги для повернення!"}))
    user_id = data[0]['user_id']
    old_user_status = get_status_name(get_user_by_id(user_id))
    res = return_of_book(data)

    if old_user_status == 'debtor' and not is_debtor(user_id):
        change_user_status(get_user_by_id(user_id), 'normal')

    if old_user_status != 'debtor' and all_books_returned(user_id):
        grant_privileges(user_id)

    for el in res:
        print(el)
    return make_response(jsonify({'message': "Книги успішно повернено"}))


def return_of_book(dict_list):
    res_list = []
    for elem in dict_list:
        order_id = elem['order_id']
        book_id = elem['book_id']
        edition = get_edition_by_book_id(book_id)
        edition_id = edition.edition_id
        if OrderBook.query.filter_by(order_id=order_id, book_id=book_id).first().return_date != None:
            res_list.append({"order_id": order_id, "edition_id": edition_id, "book_title": edition.book_title,
                             "message": "Цю книгу вже повернули"})
            continue
        num_rows_updated = OrderBook.query.filter_by(order_id=order_id, book_id=book_id).update(
            dict(return_date=date.today()))
        db.session.commit()

        edition_count = get_edition_count_obj(edition_id)
        edition_count.count_increasing()
        res_list.append({"order_id": order_id, "edition_id": edition_id, "book_title": edition.book_title,
                         "message": "Книгу успішно повернуто"})

        print('order_id: {},  edition_id: {}, book_id: {} '.format(order_id, edition_id, book_id))
        print('Current EditionCount:', edition_count.number_of_available)
        print('Return_date:', OrderBook.query.filter_by(order_id=order_id, book_id=book_id).first().return_date)
        print('-----------------------------------------------------')

    return res_list


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

@app.route("/order/issue", methods=('POST',))
def issue_order():
    # Функція для підтвердження видачі замовлення.
    # Приймає json: {"user_login": ...,    "order_id": ... }

    arrived_json = json.loads(request.data.decode('utf-8'))
    # arrived_json = {"user_login": '3', "order_id": 1}
    print(arrived_json)
    arrived_login = arrived_json["user_login"].strip()
    arrived_order_id = arrived_json["order_id"]

    order_u_login = db.session.query(Order.order_id, UserInf.user_login, Order.is_canceled).filter(
        Order.order_id == arrived_order_id,
        Order.user_id == UserInf.user_id).first()
    # 1) валідація
    # чи є такий логін?
    users = get_all_users_by_login(arrived_login)
    if len(users) == 0:
        return make_response(jsonify({'res_message': 'Немає користувачів із зазначеним логіном!'}))
    # чи є таке замовлення?
    user = users[0]
    orders = get_all_orders_by_order_id(arrived_order_id)
    if len(orders) == 0:
        return make_response(jsonify({'res_message': 'Немає замовлень із зазначеним ідентифікатором!'}))

    # чи має даний юзер дане замовлення?
    order = orders[0]
    encoded_login = hashlib.sha3_512(arrived_login.encode()).hexdigest()
    if order_u_login.user_login != encoded_login:
        return make_response(jsonify({'res_message': "Ця людина не робила цього замовлення!"}))

    # чи скасоване замовлення?
    if order.is_canceled:
        return make_response(jsonify({'res_message': 'Замовлення було скасовано!'}))

    # чи замовлення вже видане?
    if order.issue_date:
        return make_response(jsonify({'res_message': 'Замовлення вже було видано раніше!'}))

    # чи є читач боржником?
    if get_status_name(user) == 'debtor':
        # якщо боржник -- скасувати замовлення
        order.is_canceled_update(True)
        return make_response(jsonify({'res_message': 'Особа є боржником -- замовлення скасовано!'}))

    # 2) оновити запис в БД: таблиця Orders -- оновити issue_date
    order.set_issue_date()
    print(order.issue_date)
    return make_response(jsonify({'res_message': 'Замовлення було успішно видано!'}))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

@app.route('/books/delete/logic', methods=('DELETE',))
def delete_book_logic():
    book_id = request.form['id']
    book_row = get_book_row_by_book_id(book_id)
    if book_row is None:
        response = "Такого екземпляру книги немає в базі даних!"
    elif book_row.is_delete is True:
        book_title = get_edition_info_obj(book_row.edition_id).book_title
        response = "Екземпляр книги " + book_title + " вже видалений!"
    else:
        book_title = get_edition_info_obj(book_row.edition_id).book_title
        book_row.is_delete_update(new_status=True)
        edition_row = get_edition_count_obj(book_row.edition_id)
        edition_row.count_decreasing()
        response = "Один екземпляр книги " + book_title + " видалено успішно!"
    return make_response(jsonify({'response': response}))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/books/addBook/one/logic', methods=('PUT',))
def add_one_book_logic():
    edition_id = request.form['idEdition']
    book_id = request.form['idBook']
    edition_row = get_edition_info_obj(edition_id)
    if edition_row is not None:
        book_row = get_book_row_by_book_id(book_id)
        edition_count_row = get_edition_count_obj(edition_id)
        if book_row is None:
            Book.add(edition_id, book_id)
            edition_count_row.count_increasing()
            response = 'Книгу додано успішно!'
        elif book_row.is_delete is True:
            book_row.is_delete_update(new_status=False)
            edition_count_row.count_increasing()
            response = 'Книгу додано успішно!'
        else:
            response = 'Цей екземпляр вже є в базі даних!'
    else:
        response = 'Неправильно введений edition_id!'
    return make_response(jsonify({'response': response}))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/books/addBook/logic/author', methods=('PUT',))
def add_author_book_logic():
    author_name = request.form['name']
    author_surname = request.form['surname']
    author_middle_name = request.form['fatherName']  # can be null
    author_id = Author.query.filter_by(author_name=author_name, author_surname=author_surname,
                                       author_middle_name=author_middle_name).first()
    if author_id is not None:
        response = "Такий автор вже наявний в базі даних"
    else:
        Author.add(author_name, author_surname, author_middle_name)
        response = 'Доданий автор ' + author_surname + ' ' + author_name + ' ' + author_middle_name
    return make_response(jsonify({'response': response}))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
@app.route('/books/addBook/logic/genre', methods=('PUT',))
def add_genre_book_logic():
    genre = request.form['genre']
    if Genre.query.filter_by(genre=genre).first() is not None:
        response = 'Такий жанр вже наявний в базі даних!'
    else:
        Genre.add(genre)
        response = 'Жанр додано успішно!'
    return make_response(jsonify({'response': response}))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def check_authors(author_name):
    if len(author_name) == 0:
        return 'Заповніть, будь ласка, поле вводу для автора і підтвердіть додавання'

    ids = list()
    for author in author_name:
        author_name = author.split(' ')
        if len(author_name) == 2:
            name = author_name[0]
            surname = author_name[1]
            author_id = Author.query.filter_by(author_name=name, author_surname=surname,
                                               author_middle_name=None).first()
            if author_id is not None:
                ids += [author_id.author_id]
            else:
                return "В базі даних автора " + author + " немає"
        elif len(author_name) == 3:
            name = author_name[0]
            surname = author_name[1]
            middle_name = author_name[2]
            author_id = Author.query.filter_by(author_name=name, author_surname=surname,
                                               author_middle_name=middle_name).first()
            if author_id is not None:
                ids += [author_id.author_id]
            else:
                return "В базі даних автора " + author + " немає"
        else:
            return "Неккоректно введене повне ім'я автора!"
    return ids


def check_genres(genre):
    if len(genre) == 0:
        return 'Заповніть, будь ласка, поле вводу для жанру і підтвердіть додавання'

    ids = list()
    for gen in genre:
        genre_id = Genre.query.filter_by(genre=gen).first()
        if genre_id is not None:
            ids += [genre_id.genre_id]
        else:
            return "В базі даних жанру " + gen + " немає"
    return ids


@app.route('/books/addBook/logic/colection', methods=('PUT',))
def add_edition_book_logic():
    author_name = request.form['author'].split(',')[:-1]
    genre = request.form['genre'].split(',')[:-1]
    answer1 = check_authors(author_name)
    answer2 = check_genres(genre)

    if isinstance(answer1, str):
        response = answer1
    elif isinstance(answer2, str):
        response = answer2
    else:
        book_title = request.form['name']
        edition_year = request.form['year']
        edition_id = request.form['idEdition']
        if int(edition_year) > date.today().year or int(edition_year) < 868:
            response = 'Введіть коректний рік(з 868)!'
        elif EditionInf.query.filter_by(edition_id=edition_id).first() is not None:
            response = 'Такий edition_id вже існує!'
        else:
            new_edition = EditionInf.add(edition_id, book_title, edition_year)
            EditionCount.add_new_edition(edition_id)
            # додати в Edition_author
            author_list = list()
            for author_id in answer1:
                new_author = Author.query.filter_by(author_id=author_id).first()
                author_list.append(new_author)

            # додати в Edition_genre
            genre_list = list()
            for genre_id in answer2:
                new_genre = Genre.query.filter_by(genre_id=genre_id).first()
                genre_list.append(new_genre)

            new_edition.authors.extend(author_list)
            new_edition.genres.extend(genre_list)
            db.session.commit()
            response = 'Книгу додано успішно!'

    return make_response(jsonify({'response': response}))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

@app.route('/books/catalogue/orders')
def page_for_orders():
    # Сторінка для відображення замовлень користувача (її бачить не бібліотекар, а читач)
    json_orders = {"user_id": None, "orders": [], 'error_message': ''}
    if not session.get('id'):
        json_orders['error_message'] = "Авторизуйтеся!"
        return render_template('viewOrders.html', json=json_orders)

    user_id = session["id"]
    user = UserInf.query.filter_by(user_id=user_id).first()
    # показуємо лише заброньовані та не повністю повернені замовлення
    # TODO: не показувати повністю повернені замовлення!!!!!!!!!!!!!!!!!!!!!!!!
    orders = Order.query.filter_by(user_id=user_id, is_canceled=False).all()

    # складаємо json з інформацією про замовлення
    json_orders = {"user_id": user.user_id, "orders": [], 'error_message': ''}
    for order in orders:
        books = OrderBook.query.filter_by(order_id=order.order_id).all()  # можна винести в query
        books = [book.book for book in books if book.return_date == None]
        status_name = get_status_name(user)
        new_json = {
            "order_id": order.order_id,
            # "order_issue_date": order.issue_date,
            "order_in_time": status_name != 'debtor',
            "books": []
        }
        if order.issue_date and status_name == 'normal':
            new_json['order_status'] = "Видане " + str(order.issue_date) + " на 3 місяці"
        elif order.issue_date and status_name == 'privileged':
            new_json['order_status'] = "Видане " + str(order.issue_date) + " на 6 місяців"
        elif order.issue_date and status_name == 'debtor':
            new_json['order_status'] = "Строк повернення сплив -- будь ласка, поверніть книги!"
        else:
            new_json['order_status'] = "Заброньоване"

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
        json_orders['error_message'] = "У Вас немає заброньованих чи неповернених замовлень!"
    return render_template('viewOrders.html', json=json_orders)


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def grant_privileges(user_id):
    subq = db.session.query(Order.order_id,
                            func.max(OrderBook.return_date).label('max_return_date')).filter(Order.user_id == user_id,
                                                                                             Order.is_canceled == False,
                                                                                             Order.issue_date != None,
                                                                                             Order.order_id == OrderBook.order_id).group_by(
        Order.order_id).subquery('subq')
    res2 = db.session.query(subq.c.order_id, Order.issue_date, subq.c.max_return_date).filter(
        subq.c.order_id == Order.order_id).order_by(subq.c.max_return_date.desc()).limit(2).all()
    if len(res2) == 2:
        for el in res2:
            print(el.order_id, el.issue_date, el.max_return_date)

        term = {'normal': 3, 'privileged': 6}
        user = get_user_by_id(user_id)
        user_status = user.status
        num_of_months = term[user_status.status_name]
        if all([months_difference(el.max_return_date, el.issue_date) < num_of_months for el in res2]):
            change_user_status(user, 'privileged')
    return 'ok'


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def change_user_status(user, status_name):
    user.status = get_specified_status(status_name)
    db.session.commit()

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

def is_debtor(user_id):
    term = {'normal': 3, 'privileged': 6, 'debtor': 0}
    user_status = get_status_name(get_user_by_id(user_id))
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
def available_books_now(edition_id):
    # список всіх книжок одного видання
    edition_books = get_all_available_books_by_edition_id(edition_id)
    # книжки одного видання, яких немає в наявності, тому що заброньовані, або не повернені
    ordered_books = db.session.query(Book.book_id, Order.booking_date, Order.issue_date, OrderBook.return_date). \
        join(OrderBook, Book.book_id == OrderBook.book_id). \
        join(Order, Order.order_id == OrderBook.order_id). \
        filter(Book.edition_id == edition_id, OrderBook.return_date == None, Order.is_canceled == False).all()

    checked_books = list()
    for row in ordered_books:
        checked_books.append(row.book_id)

    edition_books_list = list()
    for el in edition_books:
        edition_books_list.append(el.book_id)

    A = set(edition_books_list)
    B = set(checked_books)
    books = list(A.difference(B))
    return books


def can_add(user_id):
    amount_of_books = {'normal': 10, 'privileged': 10, 'debtor': 0}
    order_list = get_all_orders_by_user_id(user_id)
    user_status = get_status_name(get_user_by_id(user_id))
    in_hands = 0
    for order in order_list:
        return_date = get_all_books_by_order_id(order.order_id)
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
        edition_amount = get_edition_count_obj(edition_id).number_of_available
        if edition_amount > 0:
            # edition_amount need to be equal to len(available_books)
            available_books = available_books_now(edition_id)
            b_order_id = available_books[-1]
            # створити новий запис в бд в Order_book
            OrderBook.add(book_id=b_order_id, order_id=order_id.order_id)
            # після бронювання книги зменшуємо кількість однакових книг
            book = get_edition_count_obj(edition_id)
            book.count_decreasing()
        else:
            book_name = get_edition_info_obj(edition_id).book_title
            return "Книги " + book_name + " немає в наявності"
    return "Замовлення пройшло успішно"


@app.route("/books/catalogue/addBook", methods=['PUT'])
def add_book_to_basket():
    session.modified = True  # для того, щоб сесія оновлювалась
    data = json.loads(request.data)
    edition_id = data['edition_id']
    if session.get('id'):
        session['basket'].append(edition_id)
        response = 'Книга додана до кошика!'
    else:
        response = 'Користувач не авторизований!'
    return make_response(jsonify({'response': response}))


@app.route("/books/basket/data", methods=['GET'])
def basket_data():
    user_id = session['id']
    chosen_books = session['basket']
    main_json = {'user_id': user_id, 'basket': []}
    for book_edition_id in chosen_books:
        book_info = get_edition_info_obj(book_edition_id)
        book_title = book_info.book_title
        edition_year = book_info.edition_year
        basket_json = {'edition_id': book_edition_id,
                       'book_title': book_title,
                       'edition_year': edition_year}
        main_json['basket'].append(basket_json)
    print(main_json)
    return make_response(jsonify(main_json))


# приймається список книг(edition_id), які користувач вирішив видалити
@app.route("/books/basket/delete", methods=['DELETE'])
def book_ordering_amount():
    data = json.loads(request.data);
    edition_id = data['edition_id']
    if session.get('id'):
        session['basket'].remove(edition_id)
    return make_response(jsonify({'response': 'Книга видалена з кошика!'}))


@app.route("/books/basket/submit", methods=['GET'])
def order_submit():
    # chosen_books - все, що додано до кошика
    chosen_books = session['basket']
    user_id = session['id']
    amount_of_chosen = len(chosen_books)
    books_can_add = can_add(user_id)
    need_to_delete = amount_of_chosen - books_can_add
    if books_can_add == 0:
        return make_response(jsonify(
            {'response': "Користувач не може забронювати книги, оскільки він або боржник, або вже замовив 10 книжок!"}))
    elif need_to_delete > 0:
        response = "Треба видалити книги зі списку кошика у кількості: " + str(need_to_delete)
        return make_response(jsonify({'response': response}))
    response = order(user_id, chosen_books)
    session['basket'].clear()
    return make_response(jsonify({'response': response}))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def collect_book_inf(editions):
    book_data_list = []
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
            "year": edition.edition_year,
            "number_of_available": get_edition_count_obj(edition.edition_id).number_of_available
        }
        book_data_list.append(book_data_output)
    return book_data_list


@app.route("/books/catalogue/return", methods=['GET'])
def take_books_data():
    if request.method == 'GET':
        book_data_list = []
        editions = EditionInf.query.all()
        book_data_list = collect_book_inf(editions)
        return make_response(jsonify({'books': book_data_list, "pagination": len(book_data_list) // 5}))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

@app.route("/books/catalogue/search/by_title", methods=['POST'])
def find_by_title():
    title_json = request.data.decode('utf-8')
    title = json.loads(title_json)['input']
    editions = EditionInf.query.filter(func.lower(EditionInf.book_title) == title.lower().strip()).all()  # можна винести в query
    book_data_list = collect_book_inf(editions)
    return make_response(jsonify({'books': book_data_list}))


@app.route("/books/catalogue/search/by_author", methods=['POST'])
def find_by_author():
    author_surname_json = request.data.decode('utf-8')
    author_surname = json.loads(author_surname_json)['input']

    editions = db.session.query(EditionInf). \
        join(t_edition_author, EditionInf.edition_id == t_edition_author.c.edition_id). \
        join(Author, t_edition_author.c.author_id == Author.author_id). \
        filter(func.lower(Author.author_surname) == author_surname.lower().strip()).all()

    book_data_list = collect_book_inf(editions)
    return make_response(jsonify({'books': book_data_list}))


@app.route("/books/catalogue/search/by_genre", methods=['POST'])
def find_by_genre():
    genre_json = request.data.decode('utf-8')
    genre = json.loads(genre_json)['input']
    editions = db.session.query(EditionInf). \
        join(t_edition_genre, EditionInf.edition_id == t_edition_genre.c.edition_id). \
        join(Genre, t_edition_genre.c.genre_id == Genre.genre_id). \
        filter(func.lower(Genre.genre) == genre.lower().strip()).all()
    book_data_list = collect_book_inf(editions)
    return make_response(jsonify({'books': book_data_list}))


@app.route("/books/catalogue/search/by_year", methods=['POST'])
def find_by_year():
    year_json = request.data.decode('utf-8')
    year = json.loads(year_json)['input']
    editions = EditionInf.query.filter_by(edition_year=year)
    book_data_list = collect_book_inf(editions)
    return make_response(jsonify({'books': book_data_list}))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

@app.route('/signup/<role_name>', methods=['POST'])
def sign_up(role_name):
    # Проводить реєстрацію користувача з даними полями.
    # Логін і пароль приходять вже в зашифрованому вигляді (sha-256).
    login = request.form["user_login"]
    password = request.form["user_password"]
    first_name = request.form["user_name"]
    last_name = request.form["surname"]
    middle_name = request.form["middle_name"]

    # шукаємо користувачів з даним логіном
    users = get_all_users_by_login(login)
    # якщо вони вже існують -- не проводимо реєстрацію
    if len(users) > 0:
        flash("Даний логін вже існує!")
        return redirect(url_for('signup'))
    else:
        # створити нового користувача
        encoded_login = hashlib.sha3_512(login.encode()).hexdigest()
        encoded_password = hashlib.sha3_512(password.encode()).hexdigest()
        new_user = UserInf.add(encoded_login, encoded_password, first_name, last_name, middle_name)
        # додати його роль в таблицю t_user_role
        added_user = get_user_by_login_and_password(login, password)
        role = get_role_by_name(role_name)
        added_user.role = role
        # додати його статус в таблицю t_user_status
        status = get_specified_status("normal")
        added_user.status = status
        # зберегти зміни
        db.session.commit()

        users = get_all_users_by_login_and_password(login, password)
        # зберегти інформацію про користувача в сесію
        user = users[0]
        session['id'] = user.user_id
        session['name'] = user.user_name
        session['role'] = user.role.role_name
        session['basket'] = []
        session['permissions'] = []
        role_permission = get_roles_permissions_by_role_id(user.role.role_id)
        permission_ids = [elem[1] for elem in role_permission]
        for perm_id in permission_ids:
            perm = get_permission_by_perm_id(perm_id)
            session['permissions'].append(perm.permission_description)
    # якщо адмін реєстрував бібліотекаря, то повернути його на сторінку адміна
    if user.role.role_name == 'librarian':
        flash("Успішно!")
        return redirect(url_for('page_for_registering_librarians'))
    else:
        return redirect(url_for('catalogue'))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
@app.route("/role/user", methods=['GET'])
def getUserRole():
    if session:
        return make_response(
            jsonify({'role': session['role'], 'permissions': session['permissions'], 'logged': session['name']}))
    else:
        return make_response(jsonify({'role': 'unlogged', 'permissions': [], 'logged': 'undefined'}))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
@app.route("/login/user", methods=['POST'])
def log_in():
    print(request.form)
    login = request.form["user_login"]
    password = request.form["user_password"]
    print(login)
    # Проводить авторизацію користувача з вказаними зашифрованими логіном і паролем.
    users = get_all_users_by_login_and_password(login, password)  # можна винести в query
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

        role_permission = get_roles_permissions_by_role_id(user.role.role_id)
        permission_ids = [elem[1] for elem in role_permission]
        for perm_id in permission_ids:
            perm = get_permission_by_perm_id(perm_id)
            session['permissions'].append(perm.permission_description)

    role = user.role.role_name
    print(session['permissions'])

    if user.role.role_name == 'librarian':
        return redirect("/books/return")
    elif user.role.role_name == 'admin':
        return redirect(url_for("page_for_registering_librarians"))
    else:
        return redirect(url_for('catalogue'))


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def check_graphіc_file():
    if not os.path.exists('static/images/analytics_gr1.png'):
        gr_issued_books(qr_issued_books())
    if not os.path.exists('static/images/analytics_gr2.png'):
        gr_debted_books()
    if not os.path.exists('static/images/analytics_gr3.png'):
        gr_debtors()
    if not os.path.exists('static/images/analytics_gr4.png'):
        gr_orders(qr_orders())


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


def all_books_returned(user_id):
    user_books = db.session.query(OrderBook.book_id, OrderBook.return_date, ).filter(Order.user_id == user_id,
                                                                                     Order.order_id == OrderBook.order_id,
                                                                                     OrderBook.return_date == None).first()
    print(user_books)
    if user_books == None:
        return True
    else:
        return False


def months_difference(date1, date2):
    # date1 -- більш пізня дата
    # date2 -- більш рання дата

    months = abs((date1.year - date2.year) * 12 + date1.month - date2.month)
    if date1.day < date2.day:
        months -= 1
    return months


def number_of_days(date1, date2):
    return abs((date1 - date2).days)


def check_availability(editions_id):
    check_list = []
    res_flag = 0
    for edition_id in editions_id:
        edition = get_edition_count_obj(edition_id)
        flag = edition.number_of_available > 0
        if flag == False:
            res_flag = 1
        check_list.append({"edition_id": edition.edition_id, "flag": flag})
    if res_flag == 0:
        return 'ok'
    else:
        return check_list


if __name__ == '__main__':
    app.run()  # , host='0.0.0.0', port=5000




