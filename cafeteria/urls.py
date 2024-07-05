from django.urls import path

#VIEWS IMPORT
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('cart/', cart, name="Cart"),
    path('cart_quantity_add/', cart_quantity_add, name="cart_quantity_add"),
    path('remove_item/', remove_item, name="remove_item"),
    path('reservation/', reservation, name="Reservation"),
    path('reservation_detail/', reservation_detail, name="Reservation_Detail"),
    path('search/', search_reservations, name='search_reservations'),
    path('signup/', signup, name="signup"),
    path('signin/<str:type>/', signin, name='signin'),
    path('signout/', signout, name="signout"),
    path('categories-cards/<str:category_name>', categories_card, name="categories-cards"),
    path('add-to-cart/', Add_to_Cart, name="add-to-cart"),
    path('card_description/<str:menu_name>', card_description, name="card_description"),
    path('checkout', checkout, name="checkout"),
    path('order-tables-user/', order_tables_user, name="order-tables-user"),
    path('manager-kitchen/', kitchen_home, name="manager-kitchen"),
    path('order-kitchen/', orders_kitchen, name="order-kitchen"),
    path('order-detail/<int:order_id>/<str:user_id>/', orders_detail, name="order-detail"),
    path('restricted-page/', restricted_page, name="restricted-page"),
    path('search-order-by-order-id/', search_order_by_order_id, name="search-order-by-order-id"),
    path('sort-by-btn/', sort_by_btn, name="sort-by-btn"),
    path('inventory-restore/', Inventory_Restore, name="inventory-restore"),
    path('change-order-status/', change_order_status, name="change-order-status"),
]