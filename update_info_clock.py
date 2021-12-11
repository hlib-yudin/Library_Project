from apscheduler.schedulers.blocking import BlockingScheduler
from models import *
#from app import db

def months_difference(date1, date2):
    # date1 -- більш пізня дата
    # date2 -- більш рання дата
    
    months = abs((date1.year - date2.year) * 12 + date1.month - date2.month)
    if date1.day < date2.day:
        months -= 1
    return months



sched = BlockingScheduler()


# кожного дня опівночі спрацьовує ця функція
@sched.scheduled_job('cron', hour=0)
def update_debtors():
    # Функція для знаходження нових боржників та зміни статусу цих користувачів на "debtor".

    debtor_counter = 0
    # знаходимо всі книги, які не повернули 
    late_books = OrderBook.query.filter(OrderBook.return_date == None)
    today = date.today()
    for book in late_books:
        # знаходимо замовлення цієї книги
        order = book.order
        # якщо замовлення скасоване  або ще не пройшло 3 місяці -- пропускаємо
        if months_difference(today, order.issue_date) < 3 or order.is_canceled:
            continue
        # знаходимо користувача, що замовив цю книгу
        user = order.user
        # якщо його статус -- не боржник, то робимо його боржником
        if user.status.status_name != "debtor":
            print(f"{datetime.now()}: {user} тепер боржник")
            user.status.status_name = "debtor"
            debtor_counter += 1

    db.session.commit()
    if debtor_counter == 0:
        print(f"{datetime.now()}: нових боржників не знайдено")

    


sched.start()
#update_debtors()