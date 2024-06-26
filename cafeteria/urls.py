from django.urls import path

#VIEWS IMPORT
from .views import *


urlpatterns = [
    path('home/', home, name="home"),
    path('cart/', cart, name="Cart"),
    path('reservation/', reservation, name="Reservation"),
    path('signup/', signup, name="signup"),
    #path('signup/<str:type>/', signin, name='signin'),
    path('signin/<str:type>/', signin, name='signin'),
    path('signout/', signout, name="signout"),
]