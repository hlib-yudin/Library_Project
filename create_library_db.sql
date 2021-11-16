/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     15.11.2021 13:50:55                          */
/*==============================================================*/


alter table if exists Book
   drop constraint if exists FK_EDITIONS_BOOKS;

alter table if exists Edition_author
   drop constraint if exists FK_AUTHORS_ED_AUTHOR;

alter table if exists Edition_author
   drop constraint if exists FK_EDITIONS_ED_AUTHOR;

alter table if exists Edition_count
   drop constraint if exists FK_EDITIONS_COUNT;

alter table if exists Edition_genre
   drop constraint if exists FK_EDITIONS_ED_GENRE;

alter table if exists Edition_genre
   drop constraint if exists FK_GENRES_ED_GENRE;

alter table if exists Order_book
   drop constraint if exists FK_ORDERS_B_ORDERS;

alter table if exists Order_book
   drop constraint if exists FK_BOOKS_ORDERS;

alter table if exists Orders
   drop constraint if exists FK_USERS_INF_ORDERS;

alter table if exists Role_permission
   drop constraint if exists FK_ROLES_PE_ROLES;

alter table if exists Role_permission
   drop constraint if exists FK_ROLES_PE_PERMISSI;

alter table if exists User_role
   drop constraint if exists FK_USERS_RO_ROLES;

alter table if exists User_role
   drop constraint if exists FK_USERS_RO_USERS_IN;

alter table if exists User_status
   drop constraint if exists FK_STA_USER_INF;

alter table if exists User_status
   drop constraint if exists FK_USER_STA_STATUS;

drop table if exists Author;

drop table if exists Book;

drop table if exists Edition_author;

drop table if exists Edition_count;

drop table if exists Edition_genre;

drop table if exists Edition_inf;

drop table if exists Genre;

drop table if exists Order_book;

drop table if exists Orders;

drop table if exists Permissions;

drop table if exists Role_permission;

drop table if exists Roles;

drop table if exists Status;

drop table if exists User_inf;

drop table if exists User_role;

drop table if exists User_status;

/*==============================================================*/
/* Table: Author                                                */
/*==============================================================*/
create table Author (
   author_id            SERIAL               not null,
   author_name          TEXT                 not null,
   author_surname       TEXT                 not null,
   author_middle_name   TEXT                 null,
   constraint PK_AUTHOR primary key (author_id),
   constraint AK_KEY_2_AUTHOR unique (author_name, author_surname, author_middle_name)
);

/*==============================================================*/
/* Table: Book                                                  */
/*==============================================================*/
create table Book (
   edition_id           TEXT                 not null,
   book_id              TEXT                 not null,
   is_delete            BOOL                 not null default FALSE,
   constraint PK_BOOK primary key (book_id),
   constraint AK_KEY_2_BOOK unique (edition_id, book_id)
);

/*==============================================================*/
/* Table: Edition_author                                        */
/*==============================================================*/
create table Edition_author (
   edition_id           TEXT                 not null,
   author_id            INT4                 not null,
   constraint PK_EDITION_AUTHOR primary key (edition_id, author_id)
);

/*==============================================================*/
/* Table: Edition_count                                         */
/*==============================================================*/
create table Edition_count (
   edition_id           TEXT                 not null,
   number_of_available  INT8                 not null,
   constraint PK_EDITION_COUNT primary key (edition_id)
);

/*==============================================================*/
/* Table: Edition_genre                                         */
/*==============================================================*/
create table Edition_genre (
   edition_id           TEXT                 not null,
   genre_id             INT4                 not null,
   constraint PK_EDITION_GENRE primary key (edition_id, genre_id)
);

/*==============================================================*/
/* Table: Edition_inf                                           */
/*==============================================================*/
create table Edition_inf (
   edition_id           TEXT                 not null,
   book_title           TEXT                 not null,
   edition_year         INT4                 not null,
   constraint PK_EDITION_INF primary key (edition_id)
);

/*==============================================================*/
/* Table: Genre                                                 */
/*==============================================================*/
create table Genre (
   genre_id             SERIAL               not null,
   genre                TEXT                 not null,
   constraint PK_GENRE primary key (genre_id),
   constraint AK_KEY_2_GENRE unique (genre)
);

/*==============================================================*/
/* Table: Order_book                                            */
/*==============================================================*/
create table Order_book (
   book_id              TEXT                 not null,
   order_id             INT4                 not null,
   return_date          DATE                 null,
   constraint PK_ORDER_BOOK primary key (book_id, order_id)
);

/*==============================================================*/
/* Table: Orders                                                */
/*==============================================================*/
create table Orders (
   order_id             SERIAL               not null,
   user_id              INT4                 not null,
   booking_date         DATE                 not null,
   issue_date           DATE                 null,
   is_canceled          BOOL                 not null default FALSE,
   constraint PK_ORDERS primary key (order_id)
);

/*==============================================================*/
/* Table: Permissions                                           */
/*==============================================================*/
create table Permissions (
   permission_id        SERIAL               not null,
   permission_description TEXT                 not null,
   constraint PK_PERMISSIONS primary key (permission_id)
);

/*==============================================================*/
/* Table: Role_permission                                       */
/*==============================================================*/
create table Role_permission (
   role_id              INT4                 not null,
   permission_id        INT4                 not null,
   constraint PK_ROLE_PERMISSION primary key (role_id, permission_id)
);

/*==============================================================*/
/* Table: Roles                                                 */
/*==============================================================*/
create table Roles (
   role_id              SERIAL               not null,
   role_name            TEXT                 not null,
   constraint PK_ROLES primary key (role_id),
   constraint AK_KEY_2_ROLES unique (role_name)
);

/*==============================================================*/
/* Table: Status                                                */
/*==============================================================*/
create table Status (
   status_id            SERIAL               not null,
   status_name          TEXT                 not null,
   constraint PK_STATUS primary key (status_id),
   constraint AK_KEY_2_STATUS unique (status_name)
);

/*==============================================================*/
/* Table: User_inf                                              */
/*==============================================================*/
create table User_inf (
   user_login           TEXT                 not null,
   user_password        TEXT                 not null,
   user_name            TEXT                 not null,
   surname              TEXT                 not null,
   middle_name          TEXT                 null,
   user_id              SERIAL               not null,
   constraint PK_USER_INF primary key (user_id),
   constraint AK_KEY_2_USER_INF unique (user_login)
);

/*==============================================================*/
/* Table: User_role                                             */
/*==============================================================*/
create table User_role (
   role_id              INT4                 not null,
   user_id              INT4                 not null,
   constraint PK_USER_ROLE primary key (role_id, user_id)
);

/*==============================================================*/
/* Table: User_status                                           */
/*==============================================================*/
create table User_status (
   user_id              INT4                 not null,
   status_id            INT4                 not null,
   constraint PK_USER_STATUS primary key (user_id, status_id)
);

alter table Book
   add constraint FK_EDITIONS_BOOKS foreign key (edition_id)
      references Edition_inf (edition_id)
      on delete restrict on update restrict;

alter table Edition_author
   add constraint FK_AUTHORS_ED_AUTHOR foreign key (author_id)
      references Author (author_id)
      on delete restrict on update restrict;

alter table Edition_author
   add constraint FK_EDITIONS_ED_AUTHOR foreign key (edition_id)
      references Edition_inf (edition_id)
      on delete restrict on update restrict;

alter table Edition_count
   add constraint FK_EDITIONS_COUNT foreign key (edition_id)
      references Edition_inf (edition_id)
      on delete restrict on update restrict;

alter table Edition_genre
   add constraint FK_EDITIONS_ED_GENRE foreign key (edition_id)
      references Edition_inf (edition_id)
      on delete restrict on update restrict;

alter table Edition_genre
   add constraint FK_GENRES_ED_GENRE foreign key (genre_id)
      references Genre (genre_id)
      on delete restrict on update restrict;

alter table Order_book
   add constraint FK_ORDERS_B_ORDERS foreign key (order_id)
      references Orders (order_id)
      on delete restrict on update restrict;

alter table Order_book
   add constraint FK_BOOKS_ORDERS foreign key (book_id)
      references Book (book_id)
      on delete restrict on update restrict;

alter table Orders
   add constraint FK_USERS_INF_ORDERS foreign key (user_id)
      references User_inf (user_id)
      on delete restrict on update restrict;

alter table Role_permission
   add constraint FK_ROLES_PE_ROLES foreign key (role_id)
      references Roles (role_id)
      on delete restrict on update restrict;

alter table Role_permission
   add constraint FK_ROLES_PE_PERMISSI foreign key (permission_id)
      references Permissions (permission_id)
      on delete restrict on update restrict;

alter table User_role
   add constraint FK_USERS_RO_ROLES foreign key (role_id)
      references Roles (role_id)
      on delete restrict on update restrict;

alter table User_role
   add constraint FK_USERS_RO_USERS_IN foreign key (user_id)
      references User_inf (user_id)
      on delete restrict on update restrict;

alter table User_status
   add constraint FK_STA_USER_INF foreign key (user_id)
      references User_inf (user_id)
      on delete restrict on update restrict;

alter table User_status
   add constraint FK_USER_STA_STATUS foreign key (status_id)
      references Status (status_id)
      on delete restrict on update restrict;



