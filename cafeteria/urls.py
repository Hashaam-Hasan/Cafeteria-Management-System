from django.urls import path

#VIEWS IMPORT
from .views import *


urlpatterns = [
    path('login', login, name="Login"),
    path('cart/', cart, name="Cart"),
]