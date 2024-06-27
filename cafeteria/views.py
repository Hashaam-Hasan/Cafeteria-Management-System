from django.shortcuts import render, redirect
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import login, authenticate, logout
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


        #Trying to get the latest user id in order to make new custom id for customer
        #Format CUS****
        try:
            last_object = User.objects.latest('id')
            last_id = last_object.id
            val = last_id[3:]
            val = str(int(val) + 1).zfill(4)  # Ensure the ID remains 4 digits
        except ObjectDoesNotExist:
            val = "00001"  # Starting value for the first user
        
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
    return render(request, 'customer/reservation.html')

