from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.register_page, name="register_page"),
    path('login/', views.login_page, name="login_page"),
    path('logout/', views.logout_user, name="logout"),

    path('home/', views.home, name='home'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('my_orders_client/', views.my_orders_client, name='my_orders_client'),
    path('balance/', views.balance, name='balance'),
    path('profile/', views.profile, name='profile'),

    path('settings/personal/<str:pk>/',
         views.personal_data, name='personal'),
    path('settings/personal_client/<str:pk>/',
         views.client_personal_data, name='personal_client'),
    path('settings/qualification/<str:pk>/',
         views.qualifications, name='qualification'),
    path('orders/', views.orders, name='orders'),


    path('client_orders/<str:pk>/',
         views.client_orders, name='client_orders'),
    path('client_orders_auction/<str:pk>/',
         views.client_orders_auction, name='client_orders_auction'),
    path('active_orders/<str:pk>/', views.active_orders, name='active_orders'),
    path('active_order/<str:pk>/',
         views.active_order, name='active_order'),
    path('client_ready_order/<str:pk>/',
         views.client_ready_order, name='client_ready_order'),


    path('create_order/', views.create_order, name='create_order'),
    path('create_order/<str:pk>/', views.create_order_for_freelancer,
         name='create_order_for_freelancer'),
    path('edit_order/<str:pk>/', views.edit_order,
         name='edit_order'),


    path('freelancers/', views.freelancers, name='freelancers'),
    path('freelancer/<str:pk>', views.freelancer, name='freelancer_page'),


    path('paypal-payment/', views.payment_complete, name='payment_completed'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='core/registration/password_reset.html'),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='core/registration/password_reset_sent.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/registration/password_reset_form.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='core/registration/password_reset_done.html'), name="password_reset_complete"),

]
