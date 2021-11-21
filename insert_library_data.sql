insert into genre (genre) values ('Художня література');
insert into genre (genre) values ('Документальна література');
insert into genre (genre) values ('Наукова фантастика');
insert into genre (genre) values ('Детектив');
insert into genre (genre) values ('Фентезі');
insert into genre (genre) values ('Містика');
insert into genre (genre) values ('Роман');
insert into genre (genre) values ('Трилер');
insert into genre (genre) values ('Історія');
insert into genre (genre) values ('Сатира');
insert into genre (genre) values ('Політика');
insert into genre (genre) values ('Хоррор');
insert into genre (genre) values ('Медицина'); 
insert into genre (genre) values ('Кулінарні книги');
insert into genre (genre) values ('Дитячі книги');
insert into genre (genre) values ('Біографія');
insert into genre (genre) values ('Автобіографія');
insert into genre (genre) values ('Бізнес і фінанси');
insert into genre (genre) values ('Словник');
insert into genre (genre) values ('Енциклопедія');
insert into genre (genre) values ('Антологія');
insert into genre (genre) values ('Кіберпанк');
insert into genre (genre) values ('Пост-апокаліптика');
insert into genre (genre) values ('Класика');
insert into genre (genre) values ('Гумор');
insert into genre (genre) values ('Подорожі');
insert into genre (genre) values ('Мистецтво');
insert into genre (genre) values ('Наука');
insert into genre (genre) values ('Підручник');
insert into genre (genre) values ('Математика');
insert into genre (genre) values ('Пригоди');
insert into genre (genre) values ('Поезія');


/* Add book 1: Математичний аналіз том 1*/                                               
insert into author (author_surname, author_name, author_middle_name) values ('Дороговцев', 'Анатолій', 'Якович');

insert into edition_inf (edition_id, book_title, edition_year) values ('5-325-00380-1', 'Математичний аналіз том 1', 1993);


insert into edition_author (edition_id, author_id) values ('5-325-00380-1', 1);

insert into edition_genre (edition_id, genre_id) values ('5-325-00380-1', 28);
insert into edition_genre (edition_id, genre_id) values ('5-325-00380-1', 30);

insert into book (edition_id, book_id) values ('5-325-00380-1', '10000001');
insert into book (edition_id, book_id) values ('5-325-00380-1', '10000002');
insert into book (edition_id, book_id) values ('5-325-00380-1', '10000003');
insert into book (edition_id, book_id) values ('5-325-00380-1', '10000004');
insert into book (edition_id, book_id) values ('5-325-00380-1', '10000005');
insert into book (edition_id, book_id) values ('5-325-00380-1', '10000006');
insert into book (edition_id, book_id) values ('5-325-00380-1', '10000007');

insert into edition_count (edition_id, number_of_available) values ('5-325-00380-1', 7);

/* Add book 2: Математичний аналіз том 2*/  
insert into author (author_surname, author_name, author_middle_name) values ('Боярчук', 'Олексій', 'Климович');  
insert into author (author_surname, author_name, author_middle_name) values ('Головач', 'Григорій', 'Петрович');  

insert into edition_inf (edition_id, book_title, edition_year) values ('5-325-00380-2', 'Математичний аналіз том 2', 1995);

insert into edition_author (edition_id, author_id) values ('5-325-00380-2', 2);
insert into edition_author (edition_id, author_id) values ('5-325-00380-2', 3);

insert into edition_genre (edition_id, genre_id) values ('5-325-00380-2', 28);
insert into edition_genre (edition_id, genre_id) values ('5-325-00380-2', 30);

insert into book (edition_id, book_id) values ('5-325-00380-2', '20000001');
insert into book (edition_id, book_id) values ('5-325-00380-2', '20000002');
insert into book (edition_id, book_id) values ('5-325-00380-2', '20000003');
insert into book (edition_id, book_id) values ('5-325-00380-2', '20000004');
insert into book (edition_id, book_id) values ('5-325-00380-2', '20000005');
insert into book (edition_id, book_id) values ('5-325-00380-2', '20000006');

insert into edition_count (edition_id, number_of_available) values ('5-325-00380-2', 6);

/* Add book 3: Гаррі Поттер і філософський камінь*/  
insert into author (author_surname, author_name) values ('Роулінг', 'Джоан');
insert into edition_inf (edition_id, book_title, edition_year) values ('6-325-01280-1', 'Гаррі Поттер і філософський камінь', 1997);

insert into edition_author (edition_id, author_id) values ('6-325-01280-1', 4);

insert into edition_genre (edition_id, genre_id) values ('6-325-01280-1', 5);
insert into edition_genre (edition_id, genre_id) values ('6-325-01280-1', 1);
insert into edition_genre (edition_id, genre_id) values ('6-325-01280-1', 31);

insert into book (edition_id, book_id) values ('6-325-01280-1', '30000001');
insert into book (edition_id, book_id) values ('6-325-01280-1', '30000002');
insert into book (edition_id, book_id) values ('6-325-01280-1', '30000003');
insert into book (edition_id, book_id) values ('6-325-01280-1', '30000004');
insert into book (edition_id, book_id) values ('6-325-01280-1', '30000005');
insert into book (edition_id, book_id) values ('6-325-01280-1', '30000006');
insert into book (edition_id, book_id) values ('6-325-01280-1', '30000007');

insert into edition_count (edition_id, number_of_available) values ('6-325-01280-1', 7);

/* Add book 4: Гаррі Поттер і таємна кімната*/  

insert into edition_inf (edition_id, book_title, edition_year) values ('6-325-01280-2', 'Гаррі Поттер і таємна кімната', 1998);

insert into edition_author (edition_id, author_id) values ('6-325-01280-2', 4);

insert into edition_genre (edition_id, genre_id) values ('6-325-01280-2', 5);
insert into edition_genre (edition_id, genre_id) values ('6-325-01280-2', 1);
insert into edition_genre (edition_id, genre_id) values ('6-325-01280-2', 31);

insert into book (edition_id, book_id) values ('6-325-01280-2', '40000001');
insert into book (edition_id, book_id) values ('6-325-01280-2', '40000002');
insert into book (edition_id, book_id) values ('6-325-01280-2', '40000003');
insert into book (edition_id, book_id) values ('6-325-01280-2', '40000004');
insert into book (edition_id, book_id) values ('6-325-01280-2', '40000005');
insert into book (edition_id, book_id) values ('6-325-01280-2', '40000006');
insert into book (edition_id, book_id) values ('6-325-01280-2', '40000007');

insert into edition_count (edition_id, number_of_available) values ('6-325-01280-2', 7);

/* Add book 5: Володар перснів: Хранителі персня*/  
insert into author (author_surname, author_name) values ('Толкін', 'Джон'); 
insert into edition_inf (edition_id, book_title, edition_year) values ('7-665-01580-1', 'Володар перснів: Хранителі персня', 1954);

insert into edition_author (edition_id, author_id) values ('7-665-01580-1', 5);

insert into edition_genre (edition_id, genre_id) values ('7-665-01580-1', 7);
insert into edition_genre (edition_id, genre_id) values ('7-665-01580-1', 5);

insert into book (edition_id, book_id) values ('7-665-01580-1', '50000001');
insert into book (edition_id, book_id) values ('7-665-01580-1', '50000002');
insert into book (edition_id, book_id) values ('7-665-01580-1', '50000003');
insert into book (edition_id, book_id) values ('7-665-01580-1', '50000004');
insert into book (edition_id, book_id) values ('7-665-01580-1', '50000005');


insert into edition_count (edition_id, number_of_available) values ('7-665-01580-1', 5);

/* Add book 6: Володар перснів: Дві вежі*/  
insert into edition_inf (edition_id, book_title, edition_year) values ('7-665-01580-2', 'Володар перснів: Дві вежі', 1954);

insert into edition_author (edition_id, author_id) values ('7-665-01580-2', 5);

insert into edition_genre (edition_id, genre_id) values ('7-665-01580-2', 7);
insert into edition_genre (edition_id, genre_id) values ('7-665-01580-2', 5);

insert into book (edition_id, book_id) values ('7-665-01580-2', '60000001');
insert into book (edition_id, book_id) values ('7-665-01580-2', '60000002');
insert into book (edition_id, book_id) values ('7-665-01580-2', '60000003');
insert into book (edition_id, book_id) values ('7-665-01580-2', '60000004');
insert into book (edition_id, book_id) values ('7-665-01580-2', '60000005');
insert into book (edition_id, book_id) values ('7-665-01580-2', '60000006');
insert into book (edition_id, book_id) values ('7-665-01580-2', '60000007');
insert into book (edition_id, book_id) values ('7-665-01580-2', '60000008');
insert into book (edition_id, book_id) values ('7-665-01580-2', '60000009');
insert into book (edition_id, book_id) values ('7-665-01580-2', '600000010');

insert into edition_count (edition_id, number_of_available) values ('7-665-01580-2', 10);

/* Add book 7: Англо-український словник*/  
insert into author (author_surname, author_name) values ('Сидоренко', 'Олеся'); --6
insert into author (author_surname, author_name) values ('Сидоренко', 'Іван'); --7
insert into author (author_surname, author_name) values ('Тесленко', 'Володимир'); --8

insert into edition_inf (edition_id, book_title, edition_year) values ('978-966-14-9349-9', 'Англо-український словник', 2015);

insert into edition_author (edition_id, author_id) values ('978-966-14-9349-9', 6);
insert into edition_author (edition_id, author_id) values ('978-966-14-9349-9', 7);
insert into edition_author (edition_id, author_id) values ('978-966-14-9349-9', 8);

insert into edition_genre (edition_id, genre_id) values ('978-966-14-9349-9', 19);

insert into book (edition_id, book_id) values ('978-966-14-9349-9', '70000001');
insert into book (edition_id, book_id) values ('978-966-14-9349-9', '70000002');
insert into book (edition_id, book_id) values ('978-966-14-9349-9', '70000003');
insert into book (edition_id, book_id) values ('978-966-14-9349-9', '70000004');
insert into book (edition_id, book_id) values ('978-966-14-9349-9', '70000005');
insert into book (edition_id, book_id) values ('978-966-14-9349-9', '70000006');
insert into book (edition_id, book_id) values ('978-966-14-9349-9', '70000007');

insert into edition_count (edition_id, number_of_available) values ('978-966-14-9349-9', 7);

/* Add book 8: */  
insert into author (author_name, author_surname) values ('Омар', 'Хайям');  --9
insert into edition_inf (edition_id, book_title, edition_year) values ('9-995-09980-1', 'Рубаї Омара Хайяма', 2018);

insert into edition_author (edition_id, author_id) values ('9-995-09980-1', 9);

insert into edition_genre (edition_id, genre_id) values ('9-995-09980-1', 21);
insert into edition_genre (edition_id, genre_id) values ('9-995-09980-1', 32);

insert into book (edition_id, book_id) values ('9-995-09980-1', '80000001');
insert into book (edition_id, book_id) values ('9-995-09980-1', '80000002');
insert into book (edition_id, book_id) values ('9-995-09980-1', '80000003');
insert into book (edition_id, book_id) values ('9-995-09980-1', '80000004');
insert into book (edition_id, book_id) values ('9-995-09980-1', '80000005');
insert into book (edition_id, book_id) values ('9-995-09980-1', '80000006');


insert into edition_count (edition_id, number_of_available) values ('9-995-09980-1', 6);

/* Add book 9: Пригоди Тома Сойєра*/  
insert into author (author_surname, author_name) values ('Твен', 'Марк'); --10
insert into edition_inf (edition_id, book_title, edition_year) values ('978-966-10-3883-6', 'Пригоди Тома Сойєра',  1876);

insert into edition_author (edition_id, author_id) values ('978-966-10-3883-6', 10);

insert into edition_genre (edition_id, genre_id) values ('978-966-10-3883-6', 7);
insert into edition_genre (edition_id, genre_id) values ('978-966-10-3883-6', 4);
insert into edition_genre (edition_id, genre_id) values ('978-966-10-3883-6', 31);
insert into edition_genre (edition_id, genre_id) values ('978-966-10-3883-6', 25);

insert into book (edition_id, book_id) values ('978-966-10-3883-6', '90000001');
insert into book (edition_id, book_id) values ('978-966-10-3883-6', '90000002');
insert into book (edition_id, book_id) values ('978-966-10-3883-6', '90000003');
insert into book (edition_id, book_id) values ('978-966-10-3883-6', '90000004');
insert into book (edition_id, book_id) values ('978-966-10-3883-6', '90000005');
insert into book (edition_id, book_id) values ('978-966-10-3883-6', '90000006');
insert into book (edition_id, book_id) values ('978-966-10-3883-6', '90000007');
insert into book (edition_id, book_id) values ('978-966-10-3883-6', '90000008');

insert into edition_count (edition_id, number_of_available) values ('978-966-10-3883-6', 8);

/* Add book 10: Лускунчик*/  
insert into author (author_surname, author_name) values ('Гофман', 'Амадей'); --11
insert into edition_inf (edition_id, book_title, edition_year) values ('118-116-11-3113-1', 'Лускунчик', 1816);

insert into edition_author (edition_id, author_id) values ('118-116-11-3113-1', 11);

insert into edition_genre (edition_id, genre_id) values ('118-116-11-3113-1', 15);
insert into edition_genre (edition_id, genre_id) values ('118-116-11-3113-1', 5);

insert into book (edition_id, book_id) values ('118-116-11-3113-1', '100000001');
insert into book (edition_id, book_id) values ('118-116-11-3113-1', '100000002');
insert into book (edition_id, book_id) values ('118-116-11-3113-1', '100000003');
insert into book (edition_id, book_id) values ('118-116-11-3113-1', '100000004');
insert into book (edition_id, book_id) values ('118-116-11-3113-1', '100000005');
insert into book (edition_id, book_id) values ('118-116-11-3113-1', '100000006');
insert into book (edition_id, book_id) values ('118-116-11-3113-1', '100000007');

insert into edition_count (edition_id, number_of_available) values ('118-116-11-3113-1', 7);



INSERT INTO Permissions (permission_description)
    VALUES  ('add books'),
            ('delete books'),
            ('register librarians'),
            ('issue/accept books'),
            ('order books');

INSERT INTO Roles (role_name)
    VALUES  ('librarian'),
            ('reader'),
            ('admin');

INSERT INTO User_inf (user_login, user_password, user_name, surname, middle_name)
    VALUES ('1', '1111', 'Богдан', 'Норкін', 'Володимирович'),
           ('2', '2222', 'Олена', 'Темнікова', 'Леонідівна'),
           ('3', '3333', 'Володимир', 'Мальчіков', 'Вікторович'),
           ('4', '4444', 'Олег', 'Чертов', 'Романович'),
           ('5', '5555', 'Тетяна', 'Ладогубець', 'Сергіївна'),
           ('6', '6666', 'Сергій', 'Сирота', NULL);

INSERT INTO Status (status_name)
    VALUES ('normal'),
           ('privileged'),
           ('debtor');

INSERT INTO Role_permission (role_id, permission_id)
    VALUES (1, 1),
           (1, 2),
           (1, 4),
           (2, 5),
           (3, 3);

INSERT INTO User_role (role_id, user_id)
    VALUES (1, 1),
           (1, 2),
           (2, 3),
           (2, 5),
           (2, 6),
           (3, 4);

INSERT INTO User_status (user_id, status_id)
    VALUES (3, 2),
           (5, 1),
           (6, 3);

------------------------------------------------------------
--Create Orders - Needn't to run this because of incorrect amount of books in future
------------------------------------------------------------
/*
insert into orders (user_id, booking_date, issue_date, is_canceled)
values (3, to_date('20-08-2020', 'DD-MM-YYYY'), 
		to_date('22-08-2020', 'DD-MM-YYYY'), false);
		
insert into order_book (book_id, order_id)
values ('10000001', 1);
UPDATE Edition_count SET number_of_available = number_of_available - 1 WHERE edition_id = '5-325-00380-1';

insert into order_book (book_id, order_id)
values ('20000001', 1);
UPDATE Edition_count SET number_of_available = number_of_available - 1 WHERE edition_id = '5-325-00380-2';

---------------------------
insert into orders (user_id, booking_date, issue_date, is_canceled)
values (3, to_date('26-08-2020', 'DD-MM-YYYY'), 
		to_date('28-08-2020', 'DD-MM-YYYY'), false);
		
insert into order_book (book_id, order_id)
values ('30000001', 2);
UPDATE Edition_count SET number_of_available = number_of_available - 1 WHERE edition_id = '6-325-01280-1';

insert into order_book (book_id, order_id, return_date)
values ('40000001', 2, to_date('12-09-2020', 'DD-MM-YYYY'));
---------------------------
insert into orders (user_id, booking_date, issue_date, is_canceled)
values (6, to_date('25-07-2020', 'DD-MM-YYYY'), 
		to_date('25-07-2020', 'DD-MM-YYYY'), false);
		
insert into order_book (book_id, order_id, return_date)
values ('50000001', 3, to_date('12-09-2020', 'DD-MM-YYYY'));

insert into order_book (book_id, order_id, return_date)
values ('60000002', 3, to_date('12-10-2020', 'DD-MM-YYYY'));
---------------------------
insert into orders (user_id, booking_date, issue_date, is_canceled)
values (6, to_date('25-07-2020', 'DD-MM-YYYY'), 
		to_date('25-07-2020', 'DD-MM-YYYY'), false);
		
insert into order_book (book_id, order_id, return_date)
values ('70000001', 4, to_date('11-09-2020', 'DD-MM-YYYY'));

--insert into order_book (book_id, order_id, return_date)
--values ('80000002', 4, to_date('11-10-2020', 'DD-MM-YYYY'));


insert into order_book (book_id, order_id)
values ('80000002', 4);
*/







