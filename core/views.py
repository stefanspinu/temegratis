from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from dateutil import parser
from django.shortcuts import get_object_or_404
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

import json
from django.http import JsonResponse

from .forms import *
from .models import *
from .decorators import unaunthenticated_user, allowed_users
from .filters import OrdersFilter, FreelancersFileter
from .utils import sidebar_left_helper, getDuplicatesWithCount

# Create your views here.


@login_required(login_url='login_page')
def home(request):
    try:
        freelancer = Freelancer.objects.get(user=request.user)
        accepted_order = AcceptedOrder.objects.all().filter(
            freelancer=freelancer)
        feedbacks = Feedback.objects.all().filter(accepted_order__in=accepted_order)

        data = sidebar_left_helper(
            accepted_order, feedbacks, request.user.freelancer.id)
        finished = data['finished']
        working_at = data['working_at']
        total_clients = data['total_clients']
        permament_clients = data['permament_clients']

        context = {
            'accepted_orders': accepted_order,
            'feedbacks': feedbacks,
            'finished': finished,
            'working_at': working_at,
            'total_clients': total_clients,
            'permament_clients': permament_clients,
        }
        return render(request, 'core/index.html', context)
    except:
        client = Client.objects.get(user=request.user)
        clients_orders = Order.objects.all().filter(client=client).count()
        in_work_orders = AcceptedOrder.objects.all().filter(
            user=request.user, paied=False).count()
        finished_orders = AcceptedOrder.objects.all().filter(
            user=request.user, paied=True).count()
        client_auction_orders = clients_orders - in_work_orders - finished_orders
        context = {
            'clients_orders': clients_orders,
            'in_work_orders': in_work_orders,
            'finished_orders': finished_orders,
            'client_auction_orders': client_auction_orders
        }
        return render(request, 'core/index.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['freelancers', 'admins'])
def personal_data(request, pk):
    freelancer = Freelancer.objects.get(id=pk)
    if request.method == 'POST':
        if 'change_avatar' in request.POST:
            change_avatar_form = ChangeAvatarPictureForm(
                request.POST, request.FILES)
            if change_avatar_form.is_valid():
                profile_pic = change_avatar_form.cleaned_data['profile_pic']
                freelancer.profile_pic = profile_pic
                freelancer.save()
                messages.success(request, 'Avatar added successfully')
                return redirect('home')
            change_name_form = ChangeNameForm()
            change_date_of_birth_form = ChangeDateOfBirthForm()
            change_contacts_form = ChangeContactForm()
            change_password_form = ChangePasswordForm()
        elif 'change_name' in request.POST:
            change_name_form = ChangeNameForm(request.POST)
            if change_name_form.is_valid():
                first_name = change_name_form.cleaned_data['first_name']
                last_name = change_name_form.cleaned_data['last_name']
                nickname = change_name_form.cleaned_data['nickname']
                freelancer.first_name = first_name
                freelancer.last_name = last_name
                freelancer.nickname = nickname
                freelancer.save()
                messages.success(request, 'Name added successfully')
                return redirect('home')
            change_avatar_form = ChangeAvatarPictureForm()
            change_date_of_birth_form = ChangeDateOfBirthForm()
            change_contacts_form = ChangeContactForm()
            change_password_form = ChangePasswordForm()
        elif 'change_date_of_birth' in request.POST:
            change_date_of_birth_form = ChangeDateOfBirthForm(request.POST)
            if change_date_of_birth_form.is_valid():
                date_of_birth = change_date_of_birth_form.cleaned_data['date_of_birth']
                freelancer.date_of_birth = date_of_birth
                freelancer.save()
                messages.success(request, 'Changed date of birth')
                return redirect('home')
            change_avatar_form = ChangeAvatarPictureForm()
            change_name_form = ChangeNameForm()
            change_contacts_form = ChangeContactForm()
            change_password_form = ChangePasswordForm()
        elif 'change_contacts' in request.POST:
            change_contacts_form = ChangeContactForm(request.POST)
            if change_contacts_form.is_valid():
                email = change_contacts_form.cleaned_data['email']
                country = change_contacts_form.cleaned_data['country']
                state = change_contacts_form.cleaned_data['state']
                address = change_contacts_form.cleaned_data['address']
                freelancer.email = email
                freelancer.country = country
                freelancer.state = state
                freelancer.address = address
                freelancer.save()
                messages.success(request, 'Contacts added successfully')
                return redirect('home')
            change_avatar_form = ChangeAvatarPictureForm()
            change_name_form = ChangeNameForm()
            change_date_of_birth_form = ChangeDateOfBirthForm()
            change_password_form = ChangePasswordForm()
        elif 'change_password' in request.POST:
            change_password_form = ChangePasswordForm(request.POST)
            if change_password_form.is_valid():
                password = change_password_form.cleaned_data['password']
                freelancer.password = password
                freelancer.save()
                messages.success(request, 'Password changed successfully')
                return redirect('home')
            change_avatar_form = ChangeAvatarPictureForm()
            change_name_form = ChangeNameForm()
            change_date_of_birth_form = ChangeDateOfBirthForm()
            change_contacts_form = ChangeContactForm()
    else:
        change_avatar_form = ChangeAvatarPictureForm()
        change_name_form = ChangeNameForm(instance=freelancer)
        change_date_of_birth_form = ChangeDateOfBirthForm(instance=freelancer)
        change_contacts_form = ChangeContactForm(instance=freelancer)
        change_password_form = ChangePasswordForm(instance=freelancer)

    context = {
        'freelancer': freelancer,
        'change_avatar_form': change_avatar_form,
        'change_name_form': change_name_form,
        'change_date_of_birth_form': change_date_of_birth_form,
        'change_contacts_form': change_contacts_form,
        'change_password_form': change_password_form
    }
    return render(request, 'core/settings/personal.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['clients'])
def client_personal_data(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == 'POST':
        if 'change_avatar' in request.POST:
            change_avatar_form = ChangeAvatarPictureFormClient(
                request.POST, request.FILES)
            if change_avatar_form.is_valid():
                profile_pic = change_avatar_form.cleaned_data['profile_pic']
                client.profile_pic = profile_pic
                client.save()
                messages.success(request, 'Avatar added successfully')
                return redirect('home')
            change_name_form = ChangeNameFormClient()
            change_date_of_birth_form = ChangeDateOfBirthFormClient()
            change_contacts_form = ChangeContactFormClient()
            change_password_form = ChangePasswordFormClient()
        elif 'change_name' in request.POST:
            change_name_form = ChangeNameFormClient(request.POST)
            if change_name_form.is_valid():
                first_name = change_name_form.cleaned_data['first_name']
                last_name = change_name_form.cleaned_data['last_name']
                nickname = change_name_form.cleaned_data['nickname']
                client.first_name = first_name
                client.last_name = last_name
                client.nickname = nickname
                client.save()
                messages.success(request, 'Name added successfully')
                return redirect('home')
            change_avatar_form = ChangeAvatarPictureFormClient()
            change_date_of_birth_form = ChangeDateOfBirthFormClient()
            change_contacts_form = ChangeContactFormClient()
            change_password_form = ChangePasswordFormClient()
        elif 'change_date_of_birth' in request.POST:
            change_date_of_birth_form = ChangeDateOfBirthFormClient(
                request.POST)
            if change_date_of_birth_form.is_valid():
                date_of_birth = change_date_of_birth_form.cleaned_data['date_of_birth']
                client.date_of_birth = date_of_birth
                client.save()
                messages.success(request, 'Changed date of birth')
                return redirect('home')
            change_avatar_form = ChangeAvatarPictureFormClient()
            change_name_form = ChangeNameFormClient()
            change_contacts_form = ChangeContactFormClient()
            change_password_form = ChangePasswordFormClient()
        elif 'change_contacts' in request.POST:
            change_contacts_form = ChangeContactFormClient(request.POST)
            if change_contacts_form.is_valid():
                email = change_contacts_form.cleaned_data['email']
                country = change_contacts_form.cleaned_data['country']
                state = change_contacts_form.cleaned_data['state']
                address = change_contacts_form.cleaned_data['address']
                client.email = email
                client.country = country
                client.state = state
                client.address = address
                client.save()
                messages.success(request, 'Contacts added successfully')
                return redirect('home')
            change_avatar_form = ChangeAvatarPictureFormClient()
            change_name_form = ChangeNameFormClient()
            change_date_of_birth_form = ChangeDateOfBirthFormClient()
            change_password_form = ChangePasswordFormClient()
        elif 'change_password' in request.POST:
            change_password_form = ChangePasswordFormClient(request.POST)
            if change_password_form.is_valid():
                password = change_password_form.cleaned_data['password']
                client.password = password
                client.save()
                messages.success(request, 'Password changed successfully')
                return redirect('home')
            change_avatar_form = ChangeAvatarPictureFormClient()
            change_name_form = ChangeNameFormClient()
            change_date_of_birth_form = ChangeDateOfBirthFormClient()
            change_contacts_form = ChangeContactFormClient()
    else:
        change_avatar_form = ChangeAvatarPictureFormClient()
        change_name_form = ChangeNameFormClient(instance=client)
        change_date_of_birth_form = ChangeDateOfBirthFormClient(
            instance=client)
        change_contacts_form = ChangeContactFormClient(instance=client)
        change_password_form = ChangePasswordFormClient(instance=client)

    context = {
        'client': client,
        'change_avatar_form': change_avatar_form,
        'change_name_form': change_name_form,
        'change_date_of_birth_form': change_date_of_birth_form,
        'change_contacts_form': change_contacts_form,
        'change_password_form': change_password_form
    }
    return render(request, 'core/settings/personal_client.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['freelancers', 'admins'])
def qualifications(request, pk):
    freelancer = Freelancer.objects.get(id=pk)
    if request.method == 'POST':
        if 'descpription' in request.POST:
            change_info_about_yourself_form = ChangeInfoAboutYourselfForm(
                request.POST)
            if change_info_about_yourself_form.is_valid():
                freelancer.short_description = change_info_about_yourself_form.cleaned_data[
                    'short_description']
                freelancer.description = change_info_about_yourself_form.cleaned_data[
                    'description']
                freelancer.save()
                messages.success(request, 'Informația a fost adăugată')
                return redirect('home')
            change_education_form = ChangeEducationForm()
            change_additional_education_form = ChangeAdditionalEducationForm()
            change_video_consultation_form = ChangeVideoConsultationForm()
            change_work_type_form = ChangeWorkTypeForm()
            change_work_category_form = ChangeWorkCategoryForm()
            change_languages_form = ChangeLanguagesForm()
        elif 'education' in request.POST:
            change_education_form = ChangeEducationForm(request.POST)
            if change_education_form.is_valid():
                freelancer.educational_institution = change_education_form.cleaned_data[
                    'educational_institution']
                freelancer.faculty = change_education_form.cleaned_data['faculty']
                freelancer.specialty = change_education_form.cleaned_data['specialty']
                freelancer.status = change_education_form.cleaned_data['status']
                freelancer.year_of_learning_end = change_education_form.cleaned_data[
                    'year_of_learning_end']
                freelancer.academic_degree = change_education_form.cleaned_data['academic_degree']
                freelancer.academic_title = change_education_form.cleaned_data['academic_title']
                freelancer.save()
                messages.success(request, 'Informația a fost adăugată')
                return redirect('home')
            change_info_about_yourself_form = ChangeInfoAboutYourselfForm()
            change_additional_education_form = ChangeAdditionalEducationForm()
            change_video_consultation_form = ChangeVideoConsultationForm()
            change_work_type_form = ChangeWorkTypeForm()
            change_work_category_form = ChangeWorkCategoryForm()
            change_languages_form = ChangeLanguagesForm()
        elif 'additional' in request.POST:
            change_additional_education_form = ChangeAdditionalEducationForm(
                request.POST)
            if change_additional_education_form.is_valid():
                freelancer.desertation_topic = change_additional_education_form.cleaned_data[
                    'desertation_topic']
                freelancer.additional_education = change_additional_education_form.cleaned_data[
                    'additional_education']
                freelancer.save()
                messages.success(request, 'Informația a fost adăugată')
                return redirect('home')
            change_info_about_yourself_form = ChangeInfoAboutYourselfForm()
            change_education_form = ChangeEducationForm()
            change_video_consultation_form = ChangeVideoConsultationForm()
            change_work_type_form = ChangeWorkTypeForm()
            change_work_category_form = ChangeWorkCategoryForm()
            change_languages_form = ChangeLanguagesForm()
        elif 'video_consultations' in request.POST:
            change_video_consultation_form = ChangeVideoConsultationForm(
                request.POST)
            if change_video_consultation_form.is_valid():
                freelancer.video_consultation = change_video_consultation_form.cleaned_data[
                    'video_consultation']
                freelancer.save()
                messages.success(request, 'Informația a fost adăugată')
                return redirect('home')
            change_info_about_yourself_form = ChangeInfoAboutYourselfForm()
            change_education_form = ChangeEducationForm()
            change_additional_education_form = ChangeAdditionalEducationForm()
            change_work_type_form = ChangeWorkTypeForm()
            change_work_category_form = ChangeWorkCategoryForm()
            change_languages_form = ChangeLanguagesForm()
        elif 'work_types' in request.POST:
            change_work_type_form = ChangeWorkTypeForm(request.POST)
            if change_work_type_form.is_valid():
                freelancer.work_type.set(
                    change_work_type_form.cleaned_data['work_type'])
                freelancer.save()
                messages.success(request, 'Informația a fost adăugată')
                return redirect('home')
            change_info_about_yourself_form = ChangeInfoAboutYourselfForm()
            change_education_form = ChangeEducationForm()
            change_additional_education_form = ChangeAdditionalEducationForm()
            change_video_consultation_form = ChangeVideoConsultationForm()
            change_work_category_form = ChangeWorkCategoryForm()
            change_languages_form = ChangeLanguagesForm()
        elif 'category_types' in request.POST:
            change_work_category_form = ChangeWorkCategoryForm(
                request.POST)
            if change_work_category_form.is_valid():
                freelancer.work_category.set(
                    change_work_category_form.cleaned_data['work_category'])
                freelancer.lessons.set(
                    change_work_category_form.cleaned_data['lessons'])
                freelancer.save()
                messages.success(request, 'Informația a fost adăugată')
                return redirect('home')
            change_info_about_yourself_form = ChangeInfoAboutYourselfForm()
            change_education_form = ChangeEducationForm()
            change_additional_education_form = ChangeAdditionalEducationForm()
            change_video_consultation_form = ChangeVideoConsultationForm()
            change_work_type_form = ChangeWorkTypeForm()
            change_languages_form = ChangeLanguagesForm()
        elif 'languages' in request.POST:
            change_languages_form = ChangeLanguagesForm(request.POST)
            if change_languages_form.is_valid():
                freelancer.languages.set(
                    change_languages_form.cleaned_data['languages'])
                freelancer.save()
                messages.success(request, 'Informația a fost adăugată')
                return redirect('home')
            change_info_about_yourself_form = ChangeInfoAboutYourselfForm()
            change_education_form = ChangeEducationForm()
            change_additional_education_form = ChangeAdditionalEducationForm()
            change_video_consultation_form = ChangeVideoConsultationForm()
            change_work_type_form = ChangeWorkTypeForm()
            change_work_category_form = ChangeWorkCategoryForm()
    else:
        change_info_about_yourself_form = ChangeInfoAboutYourselfForm(
            instance=freelancer)
        change_education_form = ChangeEducationForm(instance=freelancer)
        change_additional_education_form = ChangeAdditionalEducationForm(
            instance=freelancer)
        change_video_consultation_form = ChangeVideoConsultationForm(
            instance=freelancer)
        change_work_type_form = ChangeWorkTypeForm(instance=freelancer)
        change_work_category_form = ChangeWorkCategoryForm(instance=freelancer)
        change_languages_form = ChangeLanguagesForm(instance=freelancer)
    context = {
        'freelancer': freelancer,
        'change_info_about_yourself_form': change_info_about_yourself_form,
        'change_education_form': change_education_form,
        'change_additional_education_form': change_additional_education_form,
        'change_video_consultation_form': change_video_consultation_form,
        'change_work_type_form': change_work_type_form,
        'change_work_category_form': change_work_category_form,
        'change_languages_form': change_languages_form,
    }
    return render(request, 'core/settings/qualification.html', context)


# method_decorator(login_required, name='dispatch')
#  def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['freelancers', 'admins'])
def orders(request):
    orders = Order.objects.all().filter(
        premium=False, in_auction=True).order_by('-date_created')
    orders_premium = Order.objects.all().filter(
        premium=True, in_auction=True).order_by('-date_created')[:5]

    work_types = Work_Type.objects.all()
    lessons = Lesson.objects.all()

    orders_filter = OrdersFilter(request.GET, queryset=orders)
    orders = orders_filter.qs

    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if 'put_request' in request.POST:
        if request.user.freelancer:
            order_id = request.POST.get('order_id')
            order = Order.objects.get(id=order_id)
            freelancer = request.user.freelancer
            order.freelancers.add(freelancer)
        else:
            pass
    accepted_order = ''
    try:
        accepted_order = AcceptedOrder.objects.get(
            freelancer=request.user.freelancer)
    except:
        pass

    all_accepted_order = AcceptedOrder.objects.all()

    all_orders = Order.objects.all()

    context = {
        'all_orders': all_orders.count,
        'orders': orders,
        'orders_premium': orders_premium,
        'work_types': work_types,
        'lessons': lessons,
        'orders_filter': orders_filter,
        'accepted_order': accepted_order,
        'all_accepted_order': all_accepted_order,
        'page_obj': page_obj
    }
    return render(request, 'core/orders.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['freelancers'])
def active_orders(request, pk):
    freelancer = Freelancer.objects.get(id=pk)
    orders = []
    accepted_orders = AcceptedOrder.objects.all().filter(
        freelancer=freelancer, completed=False)
    for order in accepted_orders:
        orders.append(order.order)
    context = {
        'orders': orders
    }
    return render(request, 'core/active_orders.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['freelancers'])
def active_order(request, pk):
    order = Order.objects.get(id=pk)
    accepted_order = AcceptedOrder.objects.get(order=order)
    form = AcceptedOrderForm()
    if request.method == 'POST':
        form = AcceptedOrderForm(request.POST, request.FILES)
        if form.is_valid():
            accepted_order.description = form.cleaned_data['description']
            accepted_order.files = form.cleaned_data['files']
            accepted_order.completed = True
            accepted_order.delivered_date = datetime.now()
            accepted_order.save()
            messages.success(
                request, 'Comanda a fost trimisă spre evaluarea clientului')
            return redirect('home')

    context = {
        'order': order,
        'form': form
    }
    return render(request, 'core/active_order.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['freelancers'])
def my_orders(request):
    freelancer = Freelancer.objects.get(user=request.user)
    all_orders = AcceptedOrder.objects.all().filter(
        freelancer=freelancer)

    all_orders_active = AcceptedOrder.objects.all().filter(
        freelancer=freelancer, completed=False)

    recent_orders = AcceptedOrder.objects.all().filter(
        freelancer=freelancer).order_by('-id')[:3]

    context = {
        'all_orders': all_orders,
        'all_orders_active': all_orders_active,
        'recent_orders': recent_orders
    }
    return render(request, 'core/myorders.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['clients'])
def my_orders_client(request):
    client = request.user.client
    orders = Order.objects.all().filter(client=client)
    accepted_orders = AcceptedOrder.objects.all().filter(user=request.user)
    context = {
        'orders': orders,
        'accepted_orders': accepted_orders,
    }
    return render(request, 'core/myorders_client.html', context)


@login_required(login_url='login_page')
def balance(request):
    try:
        freelancer = Freelancer.objects.get(user=request.user)
        accepted_order = AcceptedOrder.objects.all().filter(
            freelancer=freelancer)
        feedbacks = Feedback.objects.all().filter(accepted_order__in=accepted_order)

        data = sidebar_left_helper(
            accepted_order, feedbacks, request.user.freelancer.id)
        finished = data['finished']
        working_at = data['working_at']
        total_clients = data['total_clients']
        permament_clients = data['permament_clients']

        context = {
            'accepted_orders': accepted_order,
            'feedbacks': feedbacks,
            'finished': finished,
            'working_at': working_at,
            'total_clients': total_clients,
            'permament_clients': permament_clients,
        }
    except:
        context = {}
    return render(request, 'core/balance.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['freelancers', 'admins'])
def profile(request):
    freelancer = Freelancer.objects.get(user=request.user)
    accepted_order = AcceptedOrder.objects.all().filter(
        freelancer=freelancer)
    feedbacks = Feedback.objects.all().filter(accepted_order__in=accepted_order)

    data = sidebar_left_helper(
        accepted_order, feedbacks, request.user.freelancer.id)
    positive_rating = data['positive_rating']
    negative_rating = data['negative_rating']
    percentage_positive_raiting = data['percentage_positive_raiting']
    percentage_negative_rating = data['percentage_negative_rating']
    finished = data['finished']
    working_at = data['working_at']
    total_clients = data['total_clients']
    permament_clients = data['permament_clients']
    in_time = data['in_time']
    late = data['late']
    percentage_in_time = data['percentage_in_time']
    percentage_late = data['percentage_late']

    orders = []
    for order in accepted_order:
        orders.append(order.order)

    work_types = []
    for order in orders:
        work_types.append(order.work_type.name)

    lessons = []
    for order in orders:
        lessons.append(order.lessons.name)

    dict_of_work_types = getDuplicatesWithCount(work_types)
    dict_of_lessons = getDuplicatesWithCount(lessons)

    context = {
        'freelancer': freelancer,
        'accepted_orders': accepted_order,
        'feedbacks': feedbacks,
        'finished': finished,
        'working_at': working_at,
        'total_clients': total_clients,
        'permament_clients': permament_clients,
        'positive_rating': positive_rating,
        'negative_rating': negative_rating,
        'percentage_positive_raiting': percentage_positive_raiting,
        'percentage_negative_rating': percentage_negative_rating,
        'in_time': in_time,
        'late': late,
        'percentage_in_time': percentage_in_time,
        'percentage_late': percentage_late,
        'work_types': dict_of_work_types.items(),
        'lessons': dict_of_lessons.items(),
    }
    return render(request, 'core/profile.html', context)


@ login_required(login_url='login_page')
@ allowed_users(allowed_roles=['clients'])
def client_orders(request, pk):
    client = Client.objects.get(id=pk)
    orders = Order.objects.all().filter(client=client)

    all_accepted_orders = AcceptedOrder.objects.all().filter(
        user=request.user, paied=False, completed=True)

    orders_filter = OrdersFilter(request.GET, queryset=orders)
    orders = orders_filter.qs

    context = {
        'orders': orders,
        'all_accepted_orders': all_accepted_orders,
        'orders_filter': orders_filter
    }
    return render(request, 'core/client_orders.html', context)


@ login_required(login_url='login_page')
@ allowed_users(allowed_roles=['clients'])
def client_orders_auction(request, pk):
    client = Client.objects.get(id=pk)
    orders = Order.objects.all().filter(
        client=client, acceptedorder__isnull=True)

    if 'pick_this' in request.POST:
        order_id = request.POST.get('order_id')
        freelancer_id = request.POST.get('freelancer_id')
        order = Order.objects.get(id=order_id)
        freelancer = Freelancer.objects.get(id=freelancer_id)
        accepted_order = AcceptedOrder.objects.create(user=request.user,
                                                      order=order, freelancer=freelancer)
        order.in_auction = False
        order.save()

    orders_filter = OrdersFilter(request.GET, queryset=orders)
    orders = orders_filter.qs

    context = {
        'orders': orders,
        'orders_filter': orders_filter
    }
    return render(request, 'core/client_orders_auction.html', context)


@ login_required(login_url='login_page')
@ allowed_users(allowed_roles=['clients'])
def client_ready_order(request, pk):
    accepted_order = AcceptedOrder.objects.get(id=pk)
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            rating = form.cleaned_data['rating']
            Feedback.objects.create(
                accepted_order=accepted_order, comment=comment, rating=rating)
            messages.success(request, 'Recenzia a fost trimisă')
            return redirect('home')
    context = {
        'accepted_order': accepted_order,
        'form': form
    }
    return render(request, 'core/client_ready_order.html', context)


@ login_required(login_url='login_page')
@ allowed_users(allowed_roles=['clients'])
def freelancers(request):
    freelancers = Freelancer.objects.all()

    freelancers_filter = FreelancersFileter(request.GET, queryset=freelancers)
    freelancers = freelancers_filter.qs

    context = {
        'freelancers': freelancers,
        'freelancers_filter': freelancers_filter
    }
    return render(request, 'core/freelancers.html', context)


@ login_required(login_url='login_page')
@ allowed_users(allowed_roles=['clients'])
def freelancer(request, pk):
    freelancer = Freelancer.objects.get(id=pk)
    freelancer.views = freelancer.views + 1
    freelancer.save()
    accepted_order = AcceptedOrder.objects.all().filter(
        freelancer=freelancer)
    feedbacks = Feedback.objects.all().filter(accepted_order__in=accepted_order)

    rating = 0
    positive_rating = 0
    negative_rating = 0

    data = sidebar_left_helper(
        accepted_order, feedbacks, pk)
    positive_rating = data['positive_rating']
    negative_rating = data['negative_rating']
    percentage_positive_raiting = data['percentage_positive_raiting']
    percentage_negative_rating = data['percentage_negative_rating']
    finished = data['finished']
    working_at = data['working_at']
    total_clients = data['total_clients']
    permament_clients = data['permament_clients']
    in_time = data['in_time']
    late = data['late']
    percentage_in_time = data['percentage_in_time']
    percentage_late = data['percentage_late']

    orders = []
    for order in accepted_order:
        orders.append(order.order)

    work_types = []
    for order in orders:
        work_types.append(order.work_type.name)

    lessons = []
    for order in orders:
        lessons.append(order.lessons.name)

    dict_of_work_types = getDuplicatesWithCount(work_types)
    dict_of_lessons = getDuplicatesWithCount(lessons)

    context = {
        'freelancer': freelancer,
        'accepted_orders': accepted_order,
        'feedbacks': feedbacks,
        'finished': finished,
        'working_at': working_at,
        'total_clients': total_clients,
        'permament_clients': permament_clients,
        'positive_rating': positive_rating,
        'negative_rating': negative_rating,
        'percentage_positive_raiting': percentage_positive_raiting,
        'percentage_negative_rating': percentage_negative_rating,
        'in_time': in_time,
        'late': late,
        'percentage_in_time': percentage_in_time,
        'percentage_late': percentage_late,
        'work_types': dict_of_work_types.items(),
        'lessons': dict_of_lessons.items(),
    }
    return render(request, 'core/profile_public_freelancer.html', context)


@ login_required(login_url='login_page')
@ allowed_users(allowed_roles=['clients', 'admins'])
def create_order(request):
    form = OrderForm()
    if request.method == 'POST':
        if 'place_order' in request.POST:
            form = OrderForm(request.POST, request.FILES)
            if form.is_valid():
                limit_date = form.cleaned_data['limit_date']
                title = form.cleaned_data['title']
                short_description = form.cleaned_data['short_description']
                description = form.cleaned_data['description']
                files = form.cleaned_data['files']
                min_size = form.cleaned_data['min_size']
                max_size = form.cleaned_data['max_size']
                price = form.cleaned_data['price']
                premium = form.cleaned_data['premium']
                work_type = form.cleaned_data['work_type']
                lessons = form.cleaned_data['lessons']
                order = Order.objects.create(user=request.user, date_created=timezone.now(), client=request.user.client, limit_date=limit_date, title=title, short_description=short_description,
                                             description=description, files=files, min_size=min_size, max_size=max_size, price=price, premium=premium, work_type=work_type, lessons=lessons)
                order.save()
                messages.success(request, 'Comanda a fost creată!')
                return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'core/create_order.html', context)


@ login_required(login_url='login_page')
@ allowed_users(allowed_roles=['clients', 'admins'])
def create_order_for_freelancer(request, pk):
    form = OrderForm()
    if request.method == 'POST':
        if 'place_order' in request.POST:
            form = OrderForm(request.POST, request.FILES)
            if form.is_valid():
                freelancer = []
                freelancer.append(Freelancer.objects.get(id=pk))
                limit_date = form.cleaned_data['limit_date']
                title = form.cleaned_data['title']
                short_description = form.cleaned_data['short_description']
                description = form.cleaned_data['description']
                files = form.cleaned_data['files']
                min_size = form.cleaned_data['min_size']
                max_size = form.cleaned_data['max_size']
                price = form.cleaned_data['price']
                premium = form.cleaned_data['premium']
                work_type = form.cleaned_data['work_type']
                lessons = form.cleaned_data['lessons']
                order = Order.objects.create(user=request.user, in_auction=False, date_created=timezone.now(), client=request.user.client, limit_date=limit_date, title=title, short_description=short_description,
                                             description=description, files=files, min_size=min_size, max_size=max_size, price=price, premium=premium, work_type=work_type, lessons=lessons)
                order.freelancers.set(freelancer)
                accepted_order = AcceptedOrder.objects.create(
                    order=order, freelancer=Freelancer.objects.get(id=pk), user=request.user)
                order.save()
                messages.success(request, 'Comanda a fost creată!')
                return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'core/create_order.html', context)


@ login_required(login_url='login_page')
@ allowed_users(allowed_roles=['clients', 'admins'])
def edit_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        if 'place_order' in request.POST:
            form = OrderForm(request.POST, request.FILES)
            if form.is_valid():
                order.limit_date = form.cleaned_data['limit_date']
                order.title = form.cleaned_data['title']
                order.short_description = form.cleaned_data['short_description']
                order.description = form.cleaned_data['description']
                order.files = form.cleaned_data['files']
                order.min_size = form.cleaned_data['min_size']
                order.max_size = form.cleaned_data['max_size']
                order.price = form.cleaned_data['price']
                order.premium = form.cleaned_data['premium']
                order.work_type = form.cleaned_data['work_type']
                order.lessons = form.cleaned_data['lessons']
                order.save()
                return redirect('home')
            form = OrderForm()
        elif 'delete_order' in request.POST:
            form = OrderForm(request.POST, request.FILES)
            order.delete()
            return redirect('home')
    else:
        form = OrderForm(instance=order)
    context = {
        'form': form,
        'order': order
    }
    return render(request, 'core/create_order.html', context)


@ login_required(login_url='login_page')
def payment_complete(request):
    body = json.loads(request.body)
    accepted_order = AcceptedOrder.objects.get(id=body['acceptedOrderId'])
    accepted_order.paied = True
    accepted_order.save()
    return JsonResponse('Payment completed!', safe=False)


@ unaunthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'client':
                group = Group.objects.get(name='clients')
                user.groups.add(group)
                Client.objects.create(
                    user=user,
                    first_name=username
                )
            else:
                group = Group.objects.get(name='freelancers')
                user.groups.add(group)
                Freelancer.objects.create(
                    user=user,
                    first_name=username
                )
            messages.success(request, 'Successfully registered!')
            return redirect('login_page')
    context = {
        'form': form
    }
    return render(request, 'core/registration/register.html', context)


@ unaunthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'core/registration/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_page')
