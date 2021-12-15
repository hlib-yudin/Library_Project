from models import *
from datetime import *
import numpy as np
import matplotlib.pyplot as plt


# 1
def qr_issued_books():
    res = db.session.query(func.extract('year', Order.issue_date), func.extract('month', Order.issue_date),
                            func.count(OrderBook.book_id).label('count_books')).filter(Order.issue_date != None,
                                                                                        Order.order_id == OrderBook.order_id
                                                                                       ).group_by(
                                                                                func.extract('year', Order.issue_date),
                                                                                func.extract('month', Order.issue_date)
                                                                                        ).order_by(
                                                                                func.extract('year', Order.issue_date),
                                                                                func.extract('month', Order.issue_date))
    return res.all()


def gr_issued_books(data):
    x = []
    y = []
    labels = []
    for el in data:
        x.append(datetime.strptime(str(el[1])[:-2] + '/' + str(el[0])[:-2], '%m/%Y').date())
        y.append(el[2])
        labels.append(str(el[0])[:-2] + '-' + str(el[1])[:-2])

    plt.plot(x, y)
    plt.xticks(x, labels)
    plt.gcf().autofmt_xdate()
    plt.xlabel('Місяць')
    plt.ylabel('Кількість книжок')
    plt.title('Кількість виданих книжок за часом')
    plt.show()
    # TODO: указать папку для хранения графиков
    #plt.savefig('project/image/analytics_gr1.png')
    return 0


# 2
# кількість заборгованих книжок за часом
def gr_debted_books():
    debtors_info = DebtorGraphic.query.all()
    if len(debtors_info) == 0:
        return 'no info, try next day'
    x = list()
    y = list()
    for data in debtors_info:
        x += [str(data.date_check.day)+"д "+str(data.date_check.month)+"м"]
        y += [data.books_debt]
    plt.plot(x, y)
    plt.xlabel('Час')
    plt.ylabel('Кількість заборгованих книжок')
    plt.show()
    return 'ok'


# 3
# кількість боржників за часом
def gr_debtors():
    debtors_info = DebtorGraphic.query.all()
    if len(debtors_info) == 0:
        return 'no info, try next day'
    x = list()
    y = list()
    for data in debtors_info:
        x += [str(data.date_check.day)+"д "+str(data.date_check.month)+"м"]
        y += [data.debtor_quantity]
    plt.plot(x, y)
    plt.xlabel('Час')
    plt.ylabel('Кількість боржників')
    plt.show()
    return 'ok'


# 4
# кількість !нових! замовлень за часом та кількість скасованих на поточний день
def qr_orders():
    res = db.session.query(Order.order_id, Order.booking_date, Order.is_canceled).filter(Order.issue_date == None
                                                                                         ).order_by(
        Order.booking_date)

    data = res.all()
    if len(data) == 0:
        return 0

    orders = dict()  # {date:[(is_canceled=false) ,(is_canceled=true)]}
    for row in data:
        datum = row.booking_date
        time = str(datum.day)+"д "+str(datum.month)+"м"
        if time not in orders.keys():
            orders[time] = [0, 0]
        if row.is_canceled is False:
            orders[time][0] += 1
        elif row.is_canceled is True:
            orders[time][1] += 1
    return orders


def gr_orders(orders):
    if orders == 0:
        return 'no data'

    # set width of bar
    barWidth = 0.25
    plt.subplots(figsize=(12, 8))

    canceled_false = [i[0] for i in orders.values()]
    canceled_true = [i[1] for i in orders.values()]
    times = [i for i in orders.keys()]

    # Set position of bar on X axis
    br1 = np.arange(len(canceled_false))
    br2 = [x + barWidth for x in br1]

    # Make the plot
    plt.bar(br1, canceled_false, color='g', width=barWidth,
            edgecolor='grey', label='нові замовлення')
    plt.bar(br2, canceled_true, color='r', width=barWidth,
            edgecolor='grey', label='скасовані замовлення')

    # Adding Xticks
    plt.xlabel('Час',  fontsize=15)
    plt.ylabel('Кількість нових замовлень', fontsize=15)
    plt.xticks([r + barWidth/2 for r in range(len(canceled_false))], times)

    plt.legend()
    plt.show()
    return 'ok'


gr_orders(qr_orders())



