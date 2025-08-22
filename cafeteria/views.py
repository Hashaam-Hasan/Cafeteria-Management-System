from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from datetime import date 
from .models import *


# ye sab form ki functionality h
from django.http import HttpResponseRedirect
from .forms import OrderItemStatusForm


# ye gpt wala dekhna h
# from .forms import OrderStatusForm





# Create your views here.




###################################  USER AUTHENTICATION ###################################
def signup(request):
    if request.method == 'POST':

        #Getting Values from Forms

        name = request.POST.get('name')
        email = request.POST.get('email')
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/sign_in_up.html', {'error': 'Email Exists'})
        #Trying to get the latest user id in order to make new custom id for customer
        #Format CUS****
        try:
            last_object = User.objects.latest('id')
            last_id = last_object.id
            val = last_id[3:]
            val = str(int(val) + 1).zfill(4)  # Ensure the ID remains 4 digits
        except ObjectDoesNotExist:
            val = "0001"  # Starting value for the first user
        
        customer_id = "CUS" + val


        role_type = Role.objects.get(role_name='Customer')

        
        # Create the AuthUser instance
        auth_user = AuthUser.objects.create_user(username=email, email=email, password=password)
            
        # Create the custom User instance
        custom_user = User.objects.create(id = customer_id,user=auth_user, email=email, f_name=first_name, l_name=last_name, role=role_type)

        # Authenticate and login the user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/sign_in_up.html', {'error': 'Authentication failed'})
    return render(request, 'accounts/sign_in_up.html')

def signin(request, *args, **kwargs):
#('manager')
    if request.method == "POST":

        #Getting Values from Forms
        email = request.POST.get('email')
        password = request.POST.get('password')

        #i am getting the type of user which are trying to sign in 
        sign_in_type = kwargs['type']
        
        # Authenticate and login the user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            if sign_in_type.lower() == 'customer':
                return redirect('home')
            elif sign_in_type.lower() == 'admin':
                pass
            elif sign_in_type.lower() == 'manager':
                pass
        else:
            return render(request, 'accounts/sign_in_up.html', {'error': 'Invalid-Credentials'})
    return render(request, 'accounts/sign_in_up.html')

def signout(request):

    #logout the user from the session
    logout(request)
    return redirect('signup')


###################################  Customer ###################################

def home(request, *args, **kwargs):
    
    if request.user.is_superuser:
        logout(request)
        return redirect('home')

    categories = Category.objects.all()  # Corrected variable name to 'categories'
    context = {'categories': categories}
    return render(request, 'customer/home.html', context)


def cart(request):
    return render(request, 'customer/cart.html')


def reservation(request):
    slots = Slot.objects.all()
    tables = Table.objects.all()
    context = {"slots": slots, "tables": tables}

    if request.method == "POST":
        Date = request.POST.get('date')
        table = request.POST.get('table')
        slot = request.POST.get('slot')
        user_email = request.user.email
        user = User.object.get(email = user_email)

        #for date check
        if Date and Date >= str(date.today()):
            if Reservation.objects.filter(Date = Date, table= table, slot = slot).exists():
                context["error"] = "this table is already reserved"
        else:
            Reservation.objects.create(Date = Date, table = table, slot = slot, user = user)
            context["successful"] = "Reservation is successfully created"
    else:
            context["error"] = "Reservation date must be present or in the future "
            

    reservations = Reservation.objects.all() #sari reservation context m display 
    context["reservations"] = reservations

    return render(request, 'customer/reservation.html', context)

def reservation_detail(request):
    return render(request, 'customer/reservation_detail.html')

def search_reservations(request):
    query = request.GET.get('reservation_date')
    if query:
        reservations = Reservation.objects.filter(reservation_date=query)
        print(reservations)
    else:
        reservations = Reservation.objects.all()

    reservations_list = [{
        'id': reservation.table.id,
        'reservation_date': reservation.reservation_date,
        'start_time': reservation.slot.start_time,
        'end_time': reservation.slot.end_time,
    } for reservation in reservations]

    return JsonResponse({'reservations': reservations_list})

def categories_card(request, *args, **kwargs):

    category_name = kwargs['category_name']  #{key: value}
    category = Category.objects.get(category_name=category_name) 
    categories = Category.objects.all()
    menu_items = MenuItem.objects.filter(catagory=category.id) 
    context = {'menus': menu_items, 'categories': categories}

    return render(request, 'customer/cards.html', context)


def add_to_cart(request,*args, **kwargs):
    if request.user.is_authenticated:
        menu_item_id = kwargs['menu_item_id'] 
        menu_item = MenuItem.objects.get(id = menu_item_id)
        user_email = request.user.email
        user = User.object.get(email = user_email)
        order = Order.objects.filter(user = user).latest('order_date')
        order_status = OrderStatus.objects.get(id = 1)
        if order.order_status == order_status :
            if OrderItem.objects.filter(menu = menu_item).exist():
                orderitem = OrderItem.objects.filter(menu = menu_item)
                orderitem.order_item_quantity+=1
            else:
                order_item = OrderItem.objects.create(menu = menu_item, 
                order_item_name = menu_item.menu_name,order = order, order_item_quantity = 1,
                order_item_total_price = menu_item.price)
    else:
        pass
    pass



#####################################################################################################
def order_list_view(request):
    orders = Order.objects.all()
    return render(request, 'order_kitchen.html', {'orders': orders})


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    order_statuses = OrderStatus.objects.all()
    return render(request, 'order_details.html',
                   {'order': order, 'order_items': order_items, 'order_statuses': order_statuses})



#ye youtube se seekha tha form ka pehle to ye dekhana jeeva ko implementation khud ki h 
# use: bas status update  form ki submission k zariye hogi
#form banega or usko view sambhaal lenge

# def order_detail_view(request, order_id):

#     order = get_object_or_404(Order, id=order_id)
#     order_items = OrderItem.objects.filter(order=order)
#     order_statuses = OrderStatus.objects.all()
    
#     if request.method == 'POST':
#         form = OrderItemStatusForm(request.POST)

#         if form.is_valid():
#             status = form.cleaned_data['status']
#             item_id = request.POST.get('item_id')
#             order_item = get_object_or_404(OrderItem, id=item_id)
#             order_item.order.order_status = status
#             order_item.order.save()
#             return HttpResponseRedirect(request.path_info)
#     else:
#         form = OrderItemStatusForm()
    
#     return render(request, 'order_details.html', {'order': order, 'order_items': order_items,
#                                                    'order_statuses': order_statuses, 'form': form})




#ab ye gpt wala dekhna h jeeva k saath
# def order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     order_items = OrderItem.objects.filter(order=order)
#     #return render(request, 'order_details.html', {'order': order, 'order_items': order_items})
#     if request.method == 'POST':
#         form = OrderStatusForm(request.POST, instance=order)
#         if form.is_valid():
#             form.save()
#             return redirect('order_detail', order_id=order_id)
#     else:
#         form = OrderStatusForm(instance=order)
#     return render(request, 'order_details.html', {'order': order, 'order_items': order_items, 'form': form})

