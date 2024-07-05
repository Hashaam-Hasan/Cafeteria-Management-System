from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import User, Role

def restrict_customer(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user_profile = User.objects.get(user=request.user)
                role = Role.objects.get(role_name="Customer")
                if user_profile.role == role:
                    return redirect("restricted-page")
            except Exception as e:
                print(e, request.user)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def customer_only_access(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user_profile = User.objects.get(user=request.user)
                role = Role.objects.get(role_name="Manager")
                if user_profile.role == role:
                    return redirect("restricted-page")
            except Exception as e:
                print(e, request.user)
        return view_func(request, *args, **kwargs)
    return _wrapped_view