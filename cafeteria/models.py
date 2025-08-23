from django.db import models
from django.contrib.auth.models import User as AuthUser
# Create your models here.




class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=20)  # Adjusted to remove default=None as it's not needed
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    
    email = models.CharField(max_length=200, null=True, unique=True)
    f_name = models.CharField(max_length=200, null=True)
    l_name = models.CharField(max_length=200, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username if self.user else''

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='categories/', blank=True, null=True)
    category_description = models.TextField(default=None)

    def __str__(self):
        return self.category_name

class MenuItem(models.Model):
    menu_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    catagory = models.ForeignKey(Category, on_delete=models.CASCADE)
    menu_image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.menu_name

class Inventory(models.Model):
    menu = models.OneToOneField(MenuItem, on_delete=models.CASCADE)
    inventory_quantity = models.IntegerField()
    max_level_stock = models.IntegerField(default=150)
    min_level_stock = models.IntegerField(default=50)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.menu.menu_name + " " + "Inventory"

class OrderStatus(models.Model):
    order_status_type = models.CharField(max_length=100)

    def __str__(self):
        return self.order_status_type


class Order(models.Model):
     user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
     total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
     order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
     order_date = models.DateTimeField(auto_now_add=True)
     order_type = models.CharField(max_length=200, null=True, blank=True)

     def __str__(self):
        return self.user.email + " " + "Orders"

class OrderItem(models.Model):
    menu = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    order_item_name = models.CharField(max_length=150)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_item_quantity = models.IntegerField()
    order_item_total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order_item_name

class Slot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.start_time) + "--" + str(self.end_time)

class Table(models.Model):
    capacity = models.IntegerField()
    is_table = models.BooleanField(default=True)

class Reservation(models.Model):
    reservation_date = models.DateField()
    # no_of_guests = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    is_reserve = models.BooleanField(default=False)

    def __str__(self):
        return str(self.reservation_date) + ": " + self.user.email

class Payment(models.Model):
    payment_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)


