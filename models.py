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



class EditionCount(db.Model):
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

    order_id = Column(Integer, db.Sequence('orders_order_id_seq'), primary_key=True)
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



db.create_all()

genre_1 = Genre(genre = 'Художня література')
db.session.add(genre_1)
db.session.add(Genre(genre = 'Документальна література'))
db.session.add(Genre(genre = 'Наукова фантастика'))
genre_4 = Genre(genre = 'Детектив')
db.session.add(genre_4)
genre_5 = Genre(genre = 'Фентезі')
db.session.add(genre_5)
db.session.add(Genre(genre = 'Містика'))
genre_7 = Genre(genre = 'Роман')
db.session.add(genre_7)
db.session.add(Genre(genre = 'Трилер'))
db.session.add(Genre(genre = 'Історія'))
db.session.add(Genre(genre = 'Сатира'))
db.session.add(Genre(genre = 'Політика'))
db.session.add(Genre(genre = 'Хоррор'))
db.session.add(Genre(genre = 'Медицина'))
db.session.add(Genre(genre = 'Кулінарні книги'))
genre_15 = Genre(genre = 'Дитячі книги')
db.session.add(genre_15)
db.session.add(Genre(genre = 'Біографія'))
db.session.add(Genre(genre = 'Автобіографія'))
db.session.add(Genre(genre = 'Бізнес і фінанси'))
genre_19 = Genre(genre = 'Словник')
db.session.add(genre_19)
db.session.add(Genre(genre = 'Енциклопедія'))
genre_21 = Genre(genre = 'Антологія')
db.session.add(genre_21)
db.session.add(Genre(genre = 'Кіберпанк'))
db.session.add(Genre(genre = 'Пост-апокаліптика'))
db.session.add(Genre(genre = 'Класика'))
genre_25 = Genre(genre = 'Гумор')
db.session.add(genre_25)
db.session.add(Genre(genre = 'Подорожі'))
db.session.add(Genre(genre = 'Мистецтво'))
genre_28 = Genre(genre = 'Наука')
db.session.add(genre_28)
db.session.add(Genre(genre = 'Підручник'))
genre_30 = Genre(genre = 'Математика')
db.session.add(genre_30)
genre_31 = Genre(genre = 'Пригоди')
db.session.add(genre_31)
genre_32 = Genre(genre = 'Поезія')
db.session.add(genre_32)

# Add book 1: Математичний аналіз том 1 
new_author = Author(author_surname = 'Дороговцев', author_name = 'Анатолій', author_middle_name = 'Якович')
#db.session.add(new_author)

new_edition = EditionInf(edition_id = '5-325-00380-1', book_title = 'Математичний аналіз том 1', edition_year = 1993)
new_edition.authors.append(new_author)
new_edition.genres.extend([genre_28, genre_30])
db.session.add(new_edition)

db.session.add(Book(edition_id = '5-325-00380-1', book_id = '10000001'))
db.session.add(Book(edition_id = '5-325-00380-1', book_id = '10000002'))
db.session.add(Book(edition_id = '5-325-00380-1', book_id = '10000003'))
db.session.add(Book(edition_id = '5-325-00380-1', book_id = '10000004'))
db.session.add(Book(edition_id = '5-325-00380-1', book_id = '10000005'))
db.session.add(Book(edition_id = '5-325-00380-1', book_id = '10000006'))
db.session.add(Book(edition_id = '5-325-00380-1', book_id = '10000007'))

db.session.add(EditionCount(edition_id = '5-325-00380-1', number_of_available = 7))

# Add book 2: Математичний аналіз том 2
new_author_1 = Author(author_surname = 'Боярчук', author_name = 'Олексій', author_middle_name = 'Климович')
db.session.add(new_author_1)
new_author_2 = Author(author_surname = 'Головач', author_name = 'Григорій', author_middle_name = 'Петрович')
db.session.add(new_author_2)

new_edition = EditionInf(edition_id = '5-325-00380-2', book_title = 'Математичний аналіз том 2', edition_year = 1995)
new_edition.authors.extend([new_author_1, new_author_2])
new_edition.genres.extend([genre_28, genre_30])
db.session.add(new_edition)

db.session.add(Book(edition_id = '5-325-00380-2', book_id = '20000001'))
db.session.add(Book(edition_id = '5-325-00380-2', book_id = '20000002'))
db.session.add(Book(edition_id = '5-325-00380-2', book_id = '20000003'))
db.session.add(Book(edition_id = '5-325-00380-2', book_id = '20000004'))
db.session.add(Book(edition_id = '5-325-00380-2', book_id = '20000005'))
db.session.add(Book(edition_id = '5-325-00380-2', book_id = '20000006'))

db.session.add(EditionCount(edition_id = '5-325-00380-2', number_of_available = 6))

# Add book 3: Гаррі Поттер і філософський камінь
new_author = Author(author_surname = 'Роулінг', author_name = 'Джоан')
db.session.add(new_author)

new_edition = EditionInf(edition_id = '6-325-01280-1', book_title = 'Гаррі Поттер і філософський камінь', edition_year = 1997)
new_edition.authors.extend([new_author])
new_edition.genres.extend([genre_5, genre_1, genre_31])
db.session.add(new_edition)

db.session.add(Book(edition_id = '6-325-01280-1', book_id = '30000001'))
db.session.add(Book(edition_id = '6-325-01280-1', book_id = '30000002'))
db.session.add(Book(edition_id = '6-325-01280-1', book_id = '30000003'))
db.session.add(Book(edition_id = '6-325-01280-1', book_id = '30000004'))
db.session.add(Book(edition_id = '6-325-01280-1', book_id = '30000005'))
db.session.add(Book(edition_id = '6-325-01280-1', book_id = '30000006'))
db.session.add(Book(edition_id = '6-325-01280-1', book_id = '30000007'))

db.session.add(EditionCount(edition_id = '6-325-01280-1', number_of_available = 7))

# Add book 4: Гаррі Поттер і таємна кімната
new_edition = EditionInf(edition_id = '6-325-01280-2', book_title = 'Гаррі Поттер і таємна кімната', edition_year = 1998)
new_edition.authors.extend([new_author])
new_edition.genres.extend([genre_5, genre_1, genre_31])
db.session.add(new_edition)

db.session.add(Book(edition_id = '6-325-01280-2', book_id = '40000001'))
db.session.add(Book(edition_id = '6-325-01280-2', book_id = '40000002'))
db.session.add(Book(edition_id = '6-325-01280-2', book_id = '40000003'))
db.session.add(Book(edition_id = '6-325-01280-2', book_id = '40000004'))
db.session.add(Book(edition_id = '6-325-01280-2', book_id = '40000005'))
db.session.add(Book(edition_id = '6-325-01280-2', book_id = '40000006'))
db.session.add(Book(edition_id = '6-325-01280-2', book_id = '40000007'))

db.session.add(EditionCount(edition_id = '6-325-01280-2', number_of_available = 7))

# Add book 5: Володар перснів: Хранителі персня
new_author = Author(author_surname = 'Толкін', author_name = 'Джон')
db.session.add(new_author)

new_edition = EditionInf(edition_id = '7-665-01580-1', book_title = 'Володар перснів: Хранителі персня', edition_year = 1954)
new_edition.authors.extend([new_author])
new_edition.genres.extend([genre_5, genre_7])
db.session.add(new_edition)

db.session.add(Book(edition_id = '7-665-01580-1', book_id = '50000001'))
db.session.add(Book(edition_id = '7-665-01580-1', book_id = '50000002'))
db.session.add(Book(edition_id = '7-665-01580-1', book_id = '50000003'))
db.session.add(Book(edition_id = '7-665-01580-1', book_id = '50000004'))
db.session.add(Book(edition_id = '7-665-01580-1', book_id = '50000005'))

db.session.add(EditionCount(edition_id = '7-665-01580-1', number_of_available = 5))

# Add book 6: Володар перснів: Дві вежі
new_edition = EditionInf(edition_id = '7-665-01580-2', book_title = 'Володар перснів: Дві вежі', edition_year = 1954)
new_edition.authors.extend([new_author])
new_edition.genres.extend([genre_5, genre_7])
db.session.add(new_edition)

db.session.add(Book(edition_id = '7-665-01580-2', book_id = '60000001'))
db.session.add(Book(edition_id = '7-665-01580-2', book_id = '60000002'))
db.session.add(Book(edition_id = '7-665-01580-2', book_id = '60000003'))
db.session.add(Book(edition_id = '7-665-01580-2', book_id = '60000004'))
db.session.add(Book(edition_id = '7-665-01580-2', book_id = '60000005'))
db.session.add(Book(edition_id = '7-665-01580-2', book_id = '60000006'))
db.session.add(Book(edition_id = '7-665-01580-2', book_id = '60000007'))
db.session.add(Book(edition_id = '7-665-01580-2', book_id = '60000008'))
db.session.add(Book(edition_id = '7-665-01580-2', book_id = '60000009'))
db.session.add(Book(edition_id = '7-665-01580-2', book_id = '600000010'))

db.session.add(EditionCount(edition_id = '7-665-01580-2', number_of_available = 10))

# Add book 7: Англо-український словник
new_author_1 = Author(author_surname = 'Сидоренко', author_name = 'Олеся')
db.session.add(new_author_1)
new_author_2 = Author(author_surname = 'Сидоренко', author_name = 'Іван')
db.session.add(new_author_2)
new_author_3 = Author(author_surname = 'Тесленко', author_name = 'Володимир')
db.session.add(new_author_3)

new_edition = EditionInf(edition_id = '978-966-14-9349-9', book_title = 'Англо-український словник', edition_year = 2015)
new_edition.authors.extend([new_author_1, new_author_2, new_author_3])
new_edition.genres.extend([genre_19])
db.session.add(new_edition)

db.session.add(Book(edition_id = '978-966-14-9349-9', book_id = '70000001'))
db.session.add(Book(edition_id = '978-966-14-9349-9', book_id = '70000002'))
db.session.add(Book(edition_id = '978-966-14-9349-9', book_id = '70000003'))
db.session.add(Book(edition_id = '978-966-14-9349-9', book_id = '70000004'))
db.session.add(Book(edition_id = '978-966-14-9349-9', book_id = '70000005'))
db.session.add(Book(edition_id = '978-966-14-9349-9', book_id = '70000006'))
db.session.add(Book(edition_id = '978-966-14-9349-9', book_id = '70000007'))

db.session.add(EditionCount(edition_id = '978-966-14-9349-9', number_of_available = 7))

# Add book 8:
new_author = Author(author_surname = 'Омар', author_name = 'Хайям')
db.session.add(new_author)

new_edition = EditionInf(edition_id = '9-995-09980-1', book_title = 'Рубаї Омара Хайяма', edition_year = 2018)
new_edition.authors.extend([new_author])
new_edition.genres.extend([genre_21, genre_32])
db.session.add(new_edition)

db.session.add(Book(edition_id = '9-995-09980-1', book_id = '80000001'))
db.session.add(Book(edition_id = '9-995-09980-1', book_id = '80000002'))
db.session.add(Book(edition_id = '9-995-09980-1', book_id = '80000003'))
db.session.add(Book(edition_id = '9-995-09980-1', book_id = '80000004'))
db.session.add(Book(edition_id = '9-995-09980-1', book_id = '80000005'))
db.session.add(Book(edition_id = '9-995-09980-1', book_id = '80000006'))

db.session.add(EditionCount(edition_id = '9-995-09980-1', number_of_available = 6))

# Add book 9: Пригоди Тома Сойєра
new_author = Author(author_surname = 'Твен', author_name = 'Марк')
db.session.add(new_author)

new_edition = EditionInf(edition_id = '978-966-10-3883-6', book_title = 'Пригоди Тома Сойєра', edition_year = 1876)
new_edition.authors.extend([new_author])
new_edition.genres.extend([genre_7, genre_4, genre_25, genre_31])
db.session.add(new_edition)

db.session.add(Book(edition_id = '978-966-10-3883-6', book_id = '90000001'))
db.session.add(Book(edition_id = '978-966-10-3883-6', book_id = '90000002'))
db.session.add(Book(edition_id = '978-966-10-3883-6', book_id = '90000003'))
db.session.add(Book(edition_id = '978-966-10-3883-6', book_id = '90000004'))
db.session.add(Book(edition_id = '978-966-10-3883-6', book_id = '90000005'))
db.session.add(Book(edition_id = '978-966-10-3883-6', book_id = '90000006'))
db.session.add(Book(edition_id = '978-966-10-3883-6', book_id = '90000007'))
db.session.add(Book(edition_id = '978-966-10-3883-6', book_id = '90000008'))

db.session.add(EditionCount(edition_id = '978-966-10-3883-6', number_of_available = 8))

# Add book 10: Лускунчик
new_author = Author(author_surname = 'Гофман', author_name = 'Амадей')
db.session.add(new_author)

new_edition = EditionInf(edition_id = '118-116-11-3113-1', book_title = 'Лускунчик', edition_year = 1816)
new_edition.authors.extend([new_author])
new_edition.genres.extend([genre_5, genre_15])
db.session.add(new_edition)

db.session.add(Book(edition_id = '118-116-11-3113-1', book_id = '100000001'))
db.session.add(Book(edition_id = '118-116-11-3113-1', book_id = '100000002'))
db.session.add(Book(edition_id = '118-116-11-3113-1', book_id = '100000003'))
db.session.add(Book(edition_id = '118-116-11-3113-1', book_id = '100000004'))
db.session.add(Book(edition_id = '118-116-11-3113-1', book_id = '100000005'))
db.session.add(Book(edition_id = '118-116-11-3113-1', book_id = '100000006'))
db.session.add(Book(edition_id = '118-116-11-3113-1', book_id = '100000007'))

db.session.add(EditionCount(edition_id = '118-116-11-3113-1', number_of_available = 7))

# ========================================================================

role_librarian = Role(role_name = 'librarian')
db.session.add(role_librarian)
role_reader = Role(role_name = 'reader')
db.session.add(role_reader)
role_admin = Role(role_name = 'admin')
db.session.add(role_admin)


new_permission = Permission(permission_description = 'add books')
new_permission.roles.extend([role_librarian])
db.session.add(new_permission)

new_permission = Permission(permission_description = 'delete books')
new_permission.roles.extend([role_librarian])
db.session.add(new_permission)

new_permission = Permission(permission_description = 'register librarians')
new_permission.roles.extend([role_admin])
db.session.add(new_permission)

new_permission = Permission(permission_description = 'issue/accept books')
new_permission.roles.extend([role_librarian])
db.session.add(new_permission)

new_permission = Permission(permission_description = 'order books')
new_permission.roles.extend([role_reader])
db.session.add(new_permission)


status_normal = Status(status_name = 'normal')
db.session.add(status_normal)
status_privileged = Status(status_name = 'privileged')
db.session.add(status_privileged)
status_debtor = Status(status_name = 'debtor')
db.session.add(status_debtor)


new_user = UserInf(user_login = '1', user_password = '1111', user_name='Богдан',
    surname='Норкін', middle_name='Володимирович')
new_user.role = role_librarian
db.session.add(new_user)

new_user = UserInf(user_login = '2', user_password = '2222', user_name='Олена',
    surname='Темнікова', middle_name='Леонідівна')
new_user.role = role_librarian
db.session.add(new_user)

new_user = UserInf(user_login = '3', user_password = '3333', user_name='Володимир',
    surname='Мальчиков', middle_name='Вікторович')
new_user.role = role_reader
new_user.status = status_privileged
db.session.add(new_user)

new_user = UserInf(user_login = '4', user_password = '4444', user_name='Олег',
    surname='Чертов', middle_name='Романович')
new_user.role = role_admin
db.session.add(new_user)

new_user = UserInf(user_login = '5', user_password = '5555', user_name='Тетяна',
    surname='Ладогубець', middle_name='Сергіївна')
new_user.role = role_reader
new_user.status = status_normal
db.session.add(new_user)

new_user = UserInf(user_login = '6', user_password = '6666', user_name='Сергій',
    surname='Сирота')
new_user.role = role_reader
new_user.status = status_debtor
db.session.add(new_user)


db.session.commit()