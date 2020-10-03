from django.http import HttpResponse
from django.shortcuts import redirect, render


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper_function


"""
If the decorator is expecting parameters, those parameters will be represented at the top of the nest,
Decorator has the class-based view while the wrapper function has the parameters of the class-based view
"""


def allowed_users(allowed_roles=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            role = None
            if request.user.role:
                role = request.user.role
            if role in allowed_roles:
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page.')

        return wrapper_function

    return decorator


def admin_redirect(view_func):
    def wrapper_func(request, *args, **kwargs):
        role = None
        if request.user.role:
            role = request.user.role
        if role == 'complainant':
            return view_func(request, *args, **kwargs)
        elif request.user.is_staff:
            return redirect('admin_home')


    return wrapper_func
