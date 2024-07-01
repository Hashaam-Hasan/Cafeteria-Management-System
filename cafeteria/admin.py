from django.contrib import admin
from .models import Role, User, Category, MenuItem, Inventory, Order, OrderStatus, OrderItem, Slot, Table, Reservation
# Register your models here.

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderStatus)
admin.site.register(Slot)
admin.site.register(Table)
admin.site.register(Reservation)
