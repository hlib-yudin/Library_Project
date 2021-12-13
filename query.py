from models import *
import hashlib

def get_book_row_by_book_id(book_id):
    return Book.query.filter_by(book_id=book_id).first()

def get_edition_by_book_id(book_id):
    return get_book_row_by_book_id(book_id).edition

def get_all_books_by_edition_id(edition_id):
    return Book.query.filter_by(edition_id=edition_id).all()

def get_all_available_books_by_edition_id(edition_id):
    return Book.query.filter_by(edition_id=edition_id, is_delete=False).all()

def get_edition_count_obj(edition_id):
    return EditionCount.query.filter_by(edition_id=edition_id).first()

def get_edition_info_obj(edition_id):
    return EditionInf.query.filter_by(edition_id=edition_id).first()

def get_not_cancelled_orders_by_user_id(user_id):
    return Order.query.filter_by(user_id=user_id, is_canceled=False).all()

def get_issued_orders_by_user_id(user_id):
    # Повертає всі замовлення, в яких хоча б одна книга не повернена
    orders = Order.query.filter(Order.user_id==user_id, Order.is_canceled==False,
            Order.issue_date != None).all()
    not_returned_orders = []
    for order in orders:
        books = get_all_books_by_order_id(order.order_id)
        for book in books:
            # якщо книга не повернена -- додаємо замовлення у список, переходимо до наступного замовлення
            if book.return_date == None:
                not_returned_orders.append(order)
                break
    return not_returned_orders

def get_all_orders_by_user_id(user_id):
    return Order.query.filter_by(user_id=user_id).all()

def get_all_orders_by_order_id(order_id):
    return Order.query.filter_by(order_id=order_id).all()

def get_all_books_by_order_id(order_id):
    return OrderBook.query.filter_by(order_id=order_id).all()

def get_user_by_id(user_id):
    return UserInf.query.filter_by(user_id=user_id).first()

def get_all_users_by_login(user_login):
    user_login = hashlib.sha3_512(user_login.encode()).hexdigest()
    return UserInf.query.filter_by(user_login=user_login).all()

def get_user_by_login_and_password(login, password):
    login = hashlib.sha3_512(login.encode()).hexdigest()
    password = hashlib.sha3_512(password.encode()).hexdigest()
    return UserInf.query.filter_by(user_login=login, user_password=password).first()

def get_all_users_by_login_and_password(login, password):
    login = hashlib.sha3_512(login.encode()).hexdigest()
    password = hashlib.sha3_512(password.encode()).hexdigest()
    return UserInf.query.filter_by(user_login=login, user_password=password).all()

def get_status_name(user):
    return user.status.status_name

def get_role_by_name(role_name):
    return Role.query.filter_by(role_name=role_name).first()

def get_specified_status(status_name):
    return Status.query.filter_by(status_name=status_name).first()

def get_roles_permissions_by_role_id(role_id):
    return db.session.query(t_role_permission).filter_by(role_id=role_id).all()

def get_permission_by_perm_id(perm_id):
    return Permission.query.filter_by(permission_id=perm_id).first()
