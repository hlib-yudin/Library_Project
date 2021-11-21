# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Date, ForeignKey, Integer, Table, Text, UniqueConstraint, text, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import * 

metadata = db.Model.metadata


# db.Model = declarative_base()
# metadata = db.Model.metadata


class Author(db.Model):
    __tablename__ = 'author'
    __table_args__ = (
        UniqueConstraint('author_name', 'author_surname', 'author_middle_name'),
    )

    author_id = Column(Integer, db.Sequence('author_author_id_seq'), primary_key=True)
    author_name = Column(Text, nullable=False)
    author_surname = Column(Text, nullable=False)
    author_middle_name = Column(Text)

    #editions = relationship('EditionInf', secondary='edition_author')



class EditionInf(db.Model):
    __tablename__ = 'edition_inf'

    edition_id = Column(Text, primary_key=True)
    book_title = Column(Text, nullable=False)
    edition_year = Column(Integer, nullable=False)

    genres = relationship('Genre', secondary='edition_genre')
    authors = relationship('Author', secondary='edition_author')

    # edition_count = relationship('EditionCount', uselist=False)



class EditionCount(EditionInf):
    __tablename__ = 'edition_count'

    edition_id = Column(ForeignKey('edition_inf.edition_id', ondelete='RESTRICT', onupdate='RESTRICT'),
                        primary_key=True)
    number_of_available = Column(BigInteger, nullable=False)

    def count_decreasing(self):
        self.number_of_available -= 1
        db.session.commit()

        
class Genre(db.Model):
    __tablename__ = 'genre'

    genre_id = Column(Integer, db.Sequence('genre_genre_id_seq'), primary_key=True)
    genre = Column(Text, nullable=False, unique=True)


class Permission(db.Model):
    __tablename__ = 'permissions'

    permission_id = Column(Integer, db.Sequence('permissions_permission_id_seq'), primary_key=True)
    permission_description = Column(Text, nullable=False)

    roles = relationship('Role', secondary='role_permission')


class Role(db.Model):
    __tablename__ = 'roles'

    role_id = Column(Integer, db.Sequence('roles_role_id_seq'), primary_key=True)
    role_name = Column(Text, nullable=False, unique=True)

    users = relationship('UserInf', secondary='user_role')


class Status(db.Model):
    __tablename__ = 'status'

    status_id = Column(Integer, db.Sequence('status_status_id_seq'), primary_key=True)
    status_name = Column(Text, nullable=False, unique=True)

    users = relationship('UserInf', secondary='user_status')


class UserInf(db.Model):
    __tablename__ = 'user_inf'

    user_login = Column(Text, nullable=False, unique=True)
    user_password = Column(Text, nullable=False)
    user_name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    middle_name = Column(Text)
    user_id = Column(Integer, db.Sequence('user_inf_user_id_seq'), primary_key=True)

    role = relationship("Role", secondary='user_role', uselist=False)
    status = relationship("Status", secondary='user_status', uselist=False)


class Book(db.Model):
    __tablename__ = 'book'
    __table_args__ = (
        UniqueConstraint('edition_id', 'book_id'),
    )

    edition_id = Column(ForeignKey('edition_inf.edition_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)
    book_id = Column(Text, primary_key=True)
    is_delete = Column(Boolean, nullable=False, server_default=text("false"))

    edition = relationship('EditionInf')


t_edition_author = Table(
    'edition_author', metadata,
    Column('edition_id', ForeignKey('edition_inf.edition_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False),
    Column('author_id', ForeignKey('author.author_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
)


t_edition_genre = Table(
    'edition_genre', metadata,
    Column('edition_id', ForeignKey('edition_inf.edition_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False),
    Column('genre_id', ForeignKey('genre.genre_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
)


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, server_default=text("nextval('orders_order_id_seq'::regclass)"))
    user_id = Column(ForeignKey('user_inf.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)
    booking_date = Column(Date, nullable=False)
    issue_date = Column(Date)
    is_canceled = Column(Boolean, nullable=False, server_default=text("false"))

    user = relationship('UserInf')
    
    def is_canceled_update(self, new_status):
        self.is_canceled = new_status
        db.session.commit()

    @classmethod
    def add(cls, user_id):
        new_order = Order(user_id=user_id, booking_date=date.today(), issue_date=None, is_canceled=False)
        db.session.add(new_order)
        db.session.commit()
        return new_order    


t_role_permission = Table(
    'role_permission', metadata,
    Column('role_id', ForeignKey('roles.role_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False),
    Column('permission_id', ForeignKey('permissions.permission_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
)


t_user_role = Table(
    'user_role', metadata,
    Column('role_id', ForeignKey('roles.role_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False),
    Column('user_id', ForeignKey('user_inf.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
)


t_user_status = Table(
    'user_status', metadata,
    Column('user_id', ForeignKey('user_inf.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False),
    Column('status_id', ForeignKey('status.status_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
)


class OrderBook(db.Model):
    __tablename__ = 'order_book'

    book_id = Column(ForeignKey('book.book_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    order_id = Column(ForeignKey('orders.order_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    return_date = Column(Date)

    book = relationship('Book')
    order = relationship('Order')
    
    
    @classmethod
    def add(cls, book_id, order_id):
        new_order = OrderBook(book_id=book_id, order_id=order_id, return_date=None)
        db.session.add(new_order)
        db.session.commit()
        return new_order
