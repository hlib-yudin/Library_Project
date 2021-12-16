from apscheduler.schedulers.blocking import BlockingScheduler
from query import *
from app import number_of_days  # is_debtor
from dateutil.relativedelta import *


sched = BlockingScheduler()


def is_debtor(user_id):
    term = {'normal': 3, 'privileged': 6, 'debtor': 0}
    user_status = get_status_name(get_user_by_id(user_id))
    num_of_months = term[user_status]
    is_debtor_flag = False
    verification_date = date.today() - relativedelta(months=num_of_months)
    user_books = db.session.query(func.count(OrderBook.book_id)).filter(Order.user_id == user_id,
                                                            Order.order_id == OrderBook.order_id,
                                                            OrderBook.return_date == None,
                                                            Order.issue_date != None,
                                                            Order.issue_date < verification_date
                                                            ).group_by(OrderBook.order_id).all()
    book_quan = 0
    if len(user_books) > 0:
        is_debtor_flag = True
        for book_num in user_books:
            book_quan += book_num[0]
    return is_debtor_flag, book_quan



# кожного дня опівночі спрацьовує ця функція
@sched.scheduled_job('cron', hour=0)
def update_debtors():
    # Функція для знаходження нових боржників та зміни статусу цих користувачів на "debtor".
    already_debtors = 0
    debtor_counter = 0
    books_debt = 0
    """
    today = date.today()
    # знаходимо всі книги, які не повернули 
    late_books = OrderBook.query.filter(OrderBook.return_date == None)
    today = date.today()
    for book in late_books:
        # знаходимо замовлення цієї книги
        order = book.order
        if order.issue_date is None:
            continue
        # якщо замовлення скасоване  або ще не пройшло 3 місяці -- пропускаємо
        elif months_difference(today, order.issue_date) < 3 or order.is_canceled:
            continue
        # знаходимо користувача, що замовив цю книгу
        user = order.user
        # якщо його статус -- не боржник, то робимо його боржником
        if user.status.status_name != "debtor":
            print(f"{datetime.now()}: {user} тепер боржник")
            user.status = get_specified_status("debtor")
            debtor_counter += 1
        elif user.status.status_name == "debtor":
            already_debtors += 1
    """
    
    all_users = UserInf.query.all()
    for user in all_users:
        # якщо це читач і боржник
        if user.role.role_name == "reader":
            is_debtor_flag, book_quantity = is_debtor(user.user_id)
            if is_debtor_flag:
                books_debt += book_quantity
                if user.status.status_name != "debtor":
                    print(f"{datetime.now()}: {user} тепер боржник")
                    user.status = get_specified_status("debtor")
                    debtor_counter += 1
                elif user.status.status_name == "debtor":
                    already_debtors += 1

    db.session.commit()
    DebtorGraphic.add(debtor_quantity=already_debtors + debtor_counter, books_debt=books_debt)
    if debtor_counter == 0:
        print(f"{datetime.now()}: нових боржників не знайдено")

        
# кожного дня опівночі спрацьовує ця функція
@sched.scheduled_job('cron', hour=0)
def is_canceled_change():
    allowed_booking_days = 14
    today_date = date.today()
    # треба перевірити скільки бронь вже висить
    not_issued_orders = Order.query.filter(Order.issue_date == None).all()
    canceled_orders_amount = 0
    for order in not_issued_orders:
        order_id = order.order_id
        order_date = order.booking_date
        booking_days = number_of_days(order_date, today_date)
        if allowed_booking_days < booking_days:
            # is_canceled is True
            order.is_canceled_update(new_status=True)
            CenceledOrder.add(order_id, order_date)
            print(f"{datetime.now()}: замовлення {order.order_id} скасовано")
            canceled_orders_amount += 1

    if canceled_orders_amount == 0:
        print(f"{datetime.now()}: жодного замовлення не скасовано")




@sched.scheduled_job('cron', hour=0)
def save_info_about_launch():
    # Зберігає дату запуску годинника в таблицю в БД.
    ClockLaunchCheck.add(date.today())
    print(f"{datetime.now()}: інформацію про запуск годинника збережено")


# перевіряємо при розгортанні застосунку, чи запускався сьогодні годинник, чи ні
launch_info = ClockLaunchCheck.query.filter_by(launch_date = date.today()).all()
# якщо не запускався...
if len(launch_info) == 0:
    # ...то викликаємо всі scheduled функції
    update_debtors()
    is_canceled_change()
    save_info_about_launch()



sched.start()
#update_debtors()
