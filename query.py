from models import *


def get_edition_by_book_id(book_id):
    return Book.query.filter_by(book_id=book_id).first().edition

def get_edition_count_obj(edition_id):
    return EditionCount.query.filter_by(edition_id=edition_id).first()

def get_all_books_by_order_id(order_id):
    return OrderBook.query.filter_by(order_id=order_id).all()

def get_user_by_id(user_id):
    return UserInf.query.filter_by(user_id=user_id).first()

def get_status_name(user):
    return user.status.status_name