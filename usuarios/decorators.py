from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages


def rol_requerido(*roles_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "No tienes permisos para acceder a esta página")
                return redirect(request.META.get('HTTP_REFERER', 'index_usuario'))
            
        return wrapper
    return decorator
    

    