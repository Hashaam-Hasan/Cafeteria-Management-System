from django.shortcuts import render, redirect
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from datetime import date as realdate, datetime
from django.contrib.auth.decorators import login_required

from .models import *


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


@login_required(login_url='signup')
def reservation(request):
    slots = Slot.objects.all()
    tables = Table.objects.all()
    categories = Category.objects.all()
    context = {"slots": slots, "tables": tables, 'categories': categories}
    
    if request.method == "POST":
        date = request.POST.get('date')
        table = request.POST.get('table')
        slot = request.POST.get('slot')
        user_id = request.user.email
        user = User.objects.get(email=user_id)
        print(user_id)

        date_object = datetime.strptime(date, "%Y-%m-%d").date() #This is changing the date which is in string in to datetime object
                                                                 # Because > or < this comaprison can not apply on different datatypes
        if date_object >= realdate.today():
            if not Reservation.objects.filter(reservation_date=date, table=table, slot=slot).exists():
                slot_instance = Slot.objects.get(id=slot)
                table_instance = Table.objects.get(id=table)
                Reservation.objects.create(reservation_date=date_object,user = user,table=table_instance, slot=slot_instance, is_reserve=True)
                context["error"] = 'You Reserve The Table'
                return render(request, 'customer/reservation.html', context)
            else:
                context["error"] = 'This table is already Reserve'
                return render(request, 'customer/reservation.html', context)
        else:
            context["error"] = 'The date must be latest'
            return render(request, 'customer/reservation.html', context)

    return render(request, 'customer/reservation.html', context)


@login_required(login_url='signup')
def reservation_detail(request):
    categories = Category.objects.all()
    reservations = Reservation.objects.filter(reservation_date__gte=realdate.today())
    context = {'categories': categories, 'reservations':reservations}
    return render(request, 'customer/reservation_detail.html', context)

@login_required(login_url='signup')
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

