from query import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')


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
    plt.figure()
    x = []
    y = []
    labels = []
    if len(data) == 0:
        plt.text(x=.3, y=.5, s="Даних немає!", fontdict={'size':25})
        plt.savefig('static/images/analytics_gr1.png')
        plt.close()
        return 'no info, try next day'

    for el in data:
        #print(el)
        x.append(datetime.strptime(str(int(el[1])) + '/' + str(int(el[0]))[-2:], '%m/%y').date())
        y.append(el[2])
        labels.append(str(int(el[0])) + '-' + str(int(el[1])))
    plt.bar(labels, y)
    # plt.xticks(x, labels)
    plt.gcf().autofmt_xdate()
    plt.xlabel('Місяць')
    plt.ylabel('Кількість книжок')
    plt.title('Кількість виданих книжок за часом')
    plt.savefig('static/images/analytics_gr1.png')
    plt.close()
#     plt.show()
    return 'ok'


# 2
# кількість заборгованих книжок за часом
def gr_debted_books():
    plt.figure()
    debtors_info = DebtorGraphic.query.all()
    if len(debtors_info) == 0:
        plt.text(x=.3, y=.5, s="Даних немає!", fontdict={'size':25})
        plt.savefig('static/images/analytics_gr2.png')
        plt.close()
        return 'no info, try next day'
    x = list()
    y = list()
    for data in debtors_info:
        x += [str(data.date_check)]
        y += [data.books_debt]
    plt.plot(x, y)
    plt.xlabel('Час')
    plt.ylabel('Кількість заборгованих книжок')
    plt.title('')
    plt.savefig('static/images/analytics_gr2.png')
    plt.close()
    #plt.show()
    return 'ok'


# 3
# кількість боржників за часом
def gr_debtors():
    plt.figure()
    debtors_info = DebtorGraphic.query.all()
    if len(debtors_info) == 0:
        plt.text(x=.3, y=.5, s="Даних немає!", fontdict={'size':25})
        plt.savefig('static/images/analytics_gr3.png')
        plt.close()
        return 'no info, try next day'
    x = list()
    y = list()
    for data in debtors_info:
        x += [str(data.date_check)]
        y += [data.debtor_quantity]
    plt.plot(x, y)
    plt.xlabel('Час')
    plt.ylabel('Кількість боржників')
    plt.title('')
    plt.savefig('static/images/analytics_gr3.png')
    plt.close()
    #plt.show()
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
        time = str(datum)
        if time not in orders.keys():
            orders[time] = [0, 0]
        orders[str(datum)][0] += 1
        res = db.session.query(func.count(CenceledOrder.order_id).label("count")).filter_by(
                cancel_date=datum).first()
        orders[str(datum)][1] = res.count
    return orders


def gr_orders(orders):
    plt.figure()
    if orders == 0:
        plt.text(x=.3, y=.5, s="Даних немає!", fontdict={'size':25})
        plt.savefig('static/images/analytics_gr4.png')
        plt.close()
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
    plt.title('')
    plt.savefig('static/images/analytics_gr4.png')
    plt.close()
    #plt.show()
    return 'ok'











