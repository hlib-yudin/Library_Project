from apscheduler.schedulers.blocking import BlockingScheduler
from models import *
from query import get_specified_status
from app import is_debtor, months_difference, number_of_days


sched = BlockingScheduler()


# кожного дня опівночі спрацьовує ця функція
@sched.scheduled_job('cron', hour=0)
def update_debtors():
    # Функція для знаходження нових боржників та зміни статусу цих користувачів на "debtor".
    already_debtors = 0
    debtor_counter = 0

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
            if is_debtor(user.user_id):
                if user.status.status_name != "debtor":
                    print(f"{datetime.now()}: {user} тепер боржник")
                    user.status = get_specified_status("debtor")
                    debtor_counter += 1
                elif user.status.status_name == "debtor":
                    already_debtors += 1


    db.session.commit()
    DebtorGraphic.add(debtor_quantity=already_debtors+debtor_counter)
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
        order_date = order.booking_date
        booking_days = number_of_days(order_date, today_date)
        if allowed_booking_days < booking_days:
            # is_canceled is True
            order.is_canceled_update(new_status=True)
            print(f"{datetime.now()}: замовлення {order.order_id} скасовано")
            canceled_orders_amount += 1

    if canceled_orders_amount == 0:
        print(f"{datetime.now()}: жодного замовлення не скасовано")   


sched.start()
#update_debtors()
