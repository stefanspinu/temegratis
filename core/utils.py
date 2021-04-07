from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib import messages

from .models import Order, Freelancer

from datetime import datetime


def sidebar_left_helper(accepted_order, feedbacks, pk):
    data = {}

    rating = 0
    positive_rating = 0
    negative_rating = 0
    if feedbacks:
        for feedback in feedbacks:
            if feedback.rating <= 3:
                negative_rating += 1
            else:
                positive_rating += 1

        if negative_rating < 0 and positive_rating < 0:
            pass
        else:
            rating = 100 / (negative_rating + positive_rating)

        percentage_positive_raiting = round(positive_rating * rating)
        percentage_negative_rating = round(negative_rating * rating)
    else:
        negative_rating = 0
        positive_rating = 0
        percentage_positive_raiting = 100
        percentage_negative_rating = 0

    finished = 0
    working_at = 0
    total_clients = 0
    permament_clients = 0

    for order in accepted_order:
        if order.completed:
            finished += 1
        else:
            working_at += 1

    freelancer = Freelancer.objects.get(id=pk)
    order = Order.objects.filter(freelancers=freelancer)
    orders = order.values('client').annotate(
        Count('id')).order_by().filter(id__count__gt=1).distinct()
    orders_queryset = order.filter(
        client__in=[item['client'] for item in orders])

    for _ in orders_queryset:
        total_clients += 1

    # clients that have more than 2 orders with this freelancer
    for _ in orders:
        permament_clients += 1

    time = 0
    in_time = 0
    late = 0
    for order in accepted_order:
        delivered_date = str(order.delivered_date)
        limit_date = str(order.order.limit_date)

        if delivered_date == 'None':
            delivered_date = limit_date
        else:
            if datetime.strptime(delivered_date, '%Y-%m-%d') <= datetime.strptime(limit_date, '%Y-%m-%d'):
                in_time += 1
            elif datetime.strptime(delivered_date, '%Y-%m-%d') >= datetime.strptime(limit_date, '%Y-%m-%d'):
                late += 1
            else:
                pass
    if in_time < 0 and late < 0:
        pass
    else:
        try:
            time = 100 / (in_time + late)
            percentage_in_time = round(in_time * time)
            percentage_late = round(late * time)
        except:
            time = 1
            percentage_in_time = 100
            percentage_late = 0

    data['positive_rating'] = positive_rating
    data['negative_rating'] = negative_rating
    data['percentage_positive_raiting'] = percentage_positive_raiting
    data['percentage_negative_rating'] = percentage_negative_rating
    data['finished'] = finished
    data['working_at'] = working_at
    data['total_clients'] = total_clients
    data['permament_clients'] = permament_clients
    data['in_time'] = in_time
    data['late'] = late
    data['percentage_in_time'] = percentage_in_time
    data['percentage_late'] = percentage_late

    return data


def getDuplicatesWithCount(listOfElems):
    dictOfElems = {}
    for elem in listOfElems:
        if elem in dictOfElems:
            dictOfElems[elem] += 1
        else:
            dictOfElems[elem] = 1

    total = 0
    for key, val in dictOfElems.items():
        total += val
    if total == 0:
        percentage_of_total = 100
    else:
        percentage_of_total = 100 / total

    dictOfElems = {key: round(val*percentage_of_total)
                   for key, val in dictOfElems.items()}

    return dictOfElems
