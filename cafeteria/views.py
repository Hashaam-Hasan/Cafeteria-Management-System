from django.shortcuts import render

# Create your views here.


def login(request, *args, **kwargs):
    return render(request, 'customer/home.html')


def cart(request):
    return render(request, 'customer/cart.html')

def reservation(request):
    return render(request, 'customer/reservation.html')
