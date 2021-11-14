# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Date, ForeignKey, Integer, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db



metadata = db.Model.metadata
# db.Model = declarative_base()
# metadata = db.Model.metadata


class Author(db.Model):
    __tablename__ = 'author'
    __table_args__ = (
        UniqueConstraint('author_name', 'author_surname', 'author_middle_name'),
    )

    author_id = Column(Integer, primary_key=True, server_default=text("nextval('author_author_id_seq'::regclass)"))
    author_name = Column(Text, nullable=False)
    author_surname = Column(Text, nullable=False)
    author_middle_name = Column(Text)

    editions = relationship('EditionInf', secondary='edition_author')

    def __repr__(self):
        return "<Author (author_id='%s'; author_name='%s'; author_surname='%s'; author_middle_name='%s')>" % (
            self.author_id, self.author_name, self.author_surname, self.author_middle_name)


class EditionInf(db.Model):
    __tablename__ = 'edition_inf'

    edition_id = Column(Text, primary_key=True)
    book_title = Column(Text, nullable=False)
    edition_year = Column(Integer, nullable=False)

    genres = relationship('Genre', secondary='edition_genre')
    authors = relationship('Author', secondary='edition_author')
    #edition_count = relationship('EditionCount', uselist=False)

    def __repr__(self):
        return "<EditionInf (edition_id='%s'; book_title='%s'; edition_year='%d')>" % (
            self.edition_id, self.book_title, self.edition_year)


class EditionCount(EditionInf):
    __tablename__ = 'edition_count'

    edition_id = Column(ForeignKey('edition_inf.edition_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
    number_of_available = Column(BigInteger, nullable=False)


class Genre(db.Model):
    __tablename__ = 'genre'

    genre_id = Column(Integer, primary_key=True, server_default=text("nextval('genre_genre_id_seq'::regclass)"))
    genre = Column(Text, nullable=False, unique=True)


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, server_default=text("nextval('orders_order_id_seq'::regclass)"))
    booking_date = Column(Date, nullable=False)
    issue_date = Column(Date)
    is_canceled = Column(Boolean, nullable=False, server_default=text("false"))


class Permission(db.Model):
    __tablename__ = 'permissions'

    permission_id = Column(Integer, primary_key=True, server_default=text("nextval('permissions_permission_id_seq'::regclass)"))
    permission_description = Column(Text, nullable=False)

    roles = relationship('Role', secondary='role_permission')


class Role(db.Model):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True, server_default=text("nextval('roles_role_id_seq'::regclass)"))
    role_name = Column(Text, nullable=False, unique=True)

    users = relationship('UserInf', secondary='user_role')


class Status(db.Model):
    __tablename__ = 'status'

    status_id = Column(Integer, primary_key=True, server_default=text("nextval('status_status_id_seq'::regclass)"))
    status_name = Column(Text, nullable=False, unique=True)

    users = relationship('UserInf', secondary='user_status')


class UserInf(db.Model):
    __tablename__ = 'user_inf'

    user_login = Column(Text, nullable=False, unique=True)
    user_password = Column(Text, nullable=False)
    user_name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    middle_name = Column(Text)
    user_id = Column(Integer, primary_key=True, server_default=text("nextval('user_inf_user_id_seq'::regclass)"))

    role = relationship("Role", secondary='user_role', uselist=False)
    status = relationship("Status", secondary='user_status', uselist=False)

    def __repr__(self):
        return "<UserInf (user_login='%s'; user_password='%s'; user_name='%s'; surname='%s'; middle_name='%s'; user_id='%d')>" % (
            self.user_id, self.user_password, self.user_name, self.surname, self.middle_name, self.user_id)

    


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

    user_id = Column(ForeignKey('user_inf.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    book_id = Column(ForeignKey('book.book_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    order_id = Column(ForeignKey('orders.order_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    return_date = Column(Date)

    book = relationship('Book')
    order = relationship('Order')
    user = relationship('UserInf')
