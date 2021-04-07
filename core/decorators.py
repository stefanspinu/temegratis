from django.http import HttpResponse
from django.shortcuts import redirect


def unaunthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('orders')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_function(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authoried to view this page')

            return view_func(request, *args, **kwargs)
        return wrapper_function
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'clients':
            return redirect('orders')

        if group == 'freelancers':
            return redirect('orders')

        if group == 'admins':
            return view_func(request, *args, **kwargs)
    return wrapper_function
