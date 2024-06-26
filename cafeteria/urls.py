from django.urls import path

#VIEWS IMPORT
from .views import *


urlpatterns = [
    path('login', login, name="Login"),
    path('cart/', cart, name="Cart"),
    path('reservation/', reservation, name="Reservation"),
    path('auth/', signup, name="sign_in_up")
]