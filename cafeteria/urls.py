from django.urls import path

#VIEWS IMPORT
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('cart/', cart, name="Cart"),
    path('reservation/', reservation, name="Reservation"),
    path('reservation_detail/', reservation_detail, name="Reservation_Detail"),
    path('search/', search_reservations, name='search_reservations'),
    path('signup/', signup, name="signup"),
    path('signin/<str:type>/', signin, name='signin'),
    path('signout/', signout, name="signout"),
    path('categories-cards/<str:category_name>', categories_card, name="categories-cards"),
]