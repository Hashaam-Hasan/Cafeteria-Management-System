from django.shortcuts import render, redirect
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from datetime import date as realdate, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from django.db.models import Q
from .decorators import *
from .models import *


# Create your views here.

def restricted_page(request):
    return render(request, 'customer/restricted_page.html')

# def customer_restriction(req):
#     if req.user.is_authenticated:
#         user_email = req.user.email
#         user = User.objects.get(email=user_email)
#         role = Role.objects.get(role_name="Customer")
#         print(user.role)
#         if user.role == role:
#             print("E")
#             return redirect("restricted-page")
#     return None

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
            last_object = User.objects.filter(id__contains="CUS").latest('user') 
            print(last_object)
            last_id = last_object.id
            val = last_id[3:]
            val = str(int(val) + 1).zfill(4)  # Ensure the ID remains 4 digits
        except Exception as e:
            print(e, "Enye")
            val = "0001"  # Starting value for the first user
        
        customer_id = "CUS" + val

        print(customer_id)
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
                return redirect("manager-kitchen")
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

@never_cache
@login_required(login_url='signup')
def cart(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        user = User.objects.get(email=user_email)
        orderStatus = OrderStatus.objects.filter(order_status_type="pending")[0]
        try:
            order = Order.objects.filter(user=user, order_status=orderStatus)[0]
            orderItems = OrderItem.objects.filter(order=order)
            order_item_split_name = ""
            if orderItems.exists():
                order_item_split_name = orderItems[0].order_item_name.split(" ")[0]
            categories = Category.objects.all()
            context = {'categories': categories, "orderItems": orderItems, "order":order} 
            return render(request, 'customer/cart.html', context)
        except:
            categories = Category.objects.all()
            context = {'categories': categories} 
            return render(request, 'customer/cart.html', context)


#Manipulate quantity from cart page
@login_required(login_url='signup')
def cart_quantity_add(request):

    if request.user.is_authenticated:
        query_quantity = request.GET.get('quantity')
        query_name = request.GET.get('menu_name')
        
        
        try:
            user_email = request.user.email
            user = User.objects.get(email=user_email)
            orderStatus = OrderStatus.objects.get(order_status_type='pending')
            menu = MenuItem.objects.get(menu_name=query_name)
            inventory = Inventory.objects.get(menu=menu)
            order = Order.objects.filter(user=user, order_status=orderStatus).latest('order_date')
            order_item = OrderItem.objects.filter(order=order, menu=menu)

            print(order_item[0].order_item_quantity, query_quantity, menu.menu_name)
            if order_item[0].order_item_quantity == int(query_quantity):
                    print("Enter")

                    orderItem_price = order_item[0].order_item_total_price
                    orderItem_id = order_item[0].id



                    return JsonResponse({"success":"success", 'orderItem_id':orderItem_id, "orderItem_price":orderItem_price, "order_total_price":order.total_price})

            if (inventory.inventory_quantity-(int(query_quantity)-1)) >= inventory.min_level_stock:
                
                
                
                
                # update_order_total(order)

                # print(order_item[0].order_item_quantity-int(query_quantity) != 0, order_item[0].order_item_quantity, query_quantity)

                

                if order_item[0].order_item_quantity-int(query_quantity) != 0: # 6 -  5 = 1 
                    inventory = Inventory.objects.get(menu=menu)
                    inventory.inventory_quantity -= (int(query_quantity)-order_item[0].order_item_quantity)
                    # print(inventory.inventory_quantity)
                    inventory.save()
                # print(inventory.inventory_quantity)
                
                order_item.update(order_item_quantity=query_quantity, order_item_total_price = menu.price * int(query_quantity) )


                order_items = OrderItem.objects.filter(order=order)
                
                value_price = 0
                for order_Item in order_items:
                    
                    value_price += order_Item.order_item_total_price
                
                order.total_price = value_price

                order.save()

            
                orderItem_price = order_item[0].order_item_total_price
                orderItem_id = order_item[0].id
               
    
                return JsonResponse({"success":"success", 'orderItem_id':orderItem_id, "orderItem_price":orderItem_price, "order_total_price":order.total_price})
            else:
                # if order_item[0].order_item_quantity == int(query_quantity):
                #     return JsonResponse({"success":"success"})
                print(menu.menu_name, inventory.inventory_quantity-int(query_quantity)) 
                return JsonResponse({"error":"No Stock"})

        except Exception as e:
            print(e)
            return JsonResponse({"error":"Something Went Wrong"})


#Order instance with filter
def update_order_total(order): #Helper Function
    order = order[0]
    order_items = OrderItem.objects.filter(order=order)
    print(order_items)
    aDD = 0
    for order_item in order_items:
        print(order_item.order_item_total_price)
        aDD += order_item.order_item_total_price
    print(aDD)
    order.total_price = aDD
    print(order.total_price, "Inside")
    order.save()


#Order instance with out filter
def update_order_total_wt_f(order): #Helper Function
    order_items = OrderItem.objects.filter(order=order)
    print(order_items)
    aDD = 0
    for order_item in order_items:
        print(order_item.order_item_total_price)
        aDD += order_item.order_item_total_price
    print(aDD)
    order.total_price = aDD

    order.save()
    

#Remove item from the cart
@login_required(login_url='signup')
def remove_item(request):
    order_item_id = request.GET.get("orderItemId")
    print(order_item_id)
    menu_name = OrderItem.objects.filter(id=order_item_id)[0].order_item_name
    qnt = OrderItem.objects.filter(id=order_item_id)[0].order_item_quantity #[obj]
    OrderItem.objects.filter(id=order_item_id).delete()
    user_email = request.user.email #Getting user email who is login in the corresponding sessions
    user = User.objects.get(email = user_email)
    order = Order.objects.filter(user = user).latest('order_date')
    
    menu = MenuItem.objects.get(menu_name=menu_name)
    inventory = Inventory.objects.get(menu=menu)
    inventory.inventory_quantity += qnt
    inventory.save()


    update_order_total_wt_f(order)
    order_total_price = order.total_price
    print(order_total_price, request.user.email)
    return JsonResponse({"success":"success", "order_total_price":order_total_price})


#Add To Cart Funcionality
@login_required(login_url='signup')
def Add_to_Cart(request):
    
    if request.user.is_authenticated:
        
        query = request.GET.get('menu-name')
        query1 = request.GET.get('cart-quantity') 
        

        menu_item = MenuItem.objects.get(menu_name = query) #Getting The menu A/C to click menu by customer
        user_email = request.user.email #Getting user email who is login in the corresponding sessions
        user = User.objects.get(email = user_email)
        order = Order.objects.filter(user = user) #Getting all the order
        
        inventory = Inventory.objects.get(menu=menu_item)
        if inventory.inventory_quantity >= inventory.min_level_stock :
            
            order_status = OrderStatus.objects.get(id = 1) #Getting order status (Pending)
            if order.exists():
                
                latest_order = Order.objects.filter(user = user).latest('order_date') #Getting the latest order by user to check if it is pending or complete
                if latest_order.order_status.order_status_type.lower() == order_status.order_status_type.lower() :
                    if OrderItem.objects.filter(order=latest_order,menu = menu_item).exists():
                        orderitem = OrderItem.objects.filter(order=latest_order,menu = menu_item) 

                        
                        
                        quantity = orderitem[0].order_item_quantity
                        if query1 is None:
                            orderitem.update(order_item_quantity=quantity+1, order_item_total_price = menu_item.price * (quantity + 1)) 
                            inventory.inventory_quantity -= 1
                            inventory.save()
                        else:
                            
                            orderitem.update(order_item_quantity=quantity+int(query1), order_item_total_price = menu_item.price * (quantity + 1)) 
                            inventory.inventory_quantity -= int(query1)
                            inventory.save()
                        update_order_total_wt_f(latest_order) 
                        return JsonResponse({"success":"Successfully Updated", "check":False})
                    else:
                        order_item = OrderItem.objects.create(menu = menu_item, 
                        order_item_name = menu_item.menu_name,order = latest_order, order_item_quantity = 1,
                        order_item_total_price = menu_item.price)
                        inventory.inventory_quantity -= 1
                        inventory.save()
                        update_order_total_wt_f(latest_order) 
                        return JsonResponse({"success":"Successfully Added", "check":False})
                else:
                    
                    new_order = Order.objects.create(user=user, total_price=menu_item.price, order_status=order_status)
                    new_order_item = OrderItem.objects.create(menu = menu_item, 
                            order_item_name = menu_item.menu_name,order = new_order, order_item_quantity = 1,
                            order_item_total_price = menu_item.price)
                    return JsonResponse({"success":"Successfully Created", "check":False})
            else:
                    
                    new_order = Order.objects.create(user=user, total_price=menu_item.price, order_status=order_status)
                    new_order_item = OrderItem.objects.create(menu = menu_item, 
                            order_item_name = menu_item.menu_name,order = new_order, order_item_quantity = 1,
                            order_item_total_price = menu_item.price)
                    return JsonResponse({"success":"Successfully Created", "check":False})
        else: 
            
            return JsonResponse({"error": "No Stock", "check":True})   
    return JsonResponse({'error': 'Try Again'})



def card_description(request, *args, **kwargs):

    categories = Category.objects.all()
    menuName = kwargs['menu_name'] 
    print(menuName)
    menu_item = MenuItem.objects.get(menu_name=menuName)
    inventory = Inventory.objects.get(menu=menu_item)
    stock = inventory.inventory_quantity >= inventory.min_level_stock

    print(menu_item.catagory.category_name)

    context = {'categories': categories, "menus": menu_item, 'stock':stock}
    return render(request, 'customer/card_description.html', context)


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

@never_cache
@login_required(login_url='signup')
def checkout(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        user = User.objects.get(email=user_email)
        categories = Category.objects.all()
        order = Order.objects.filter(user=user).latest('order_date')
        
        orderStatus_pending = OrderStatus.objects.get(order_status_type='pending')
        context = {"user":user, "order":order, 'categories':categories, "orderStatus":orderStatus_pending} 
        if order.order_status == orderStatus_pending:
            order_item = OrderItem.objects.filter(order=order)
            context["order_item"] = order_item

        if request.method == "POST":
            address = request.POST.get('address')
            contactno = request.POST.get("ContactNo")
            city = request.POST.get("city")
            orderType = request.POST.get("OrderType")
            payment_type = request.POST.get("payment_type")

            print(payment_type)

            orderStatus = OrderStatus.objects.get(order_status_type='process')

            
            order.order_type = orderType
            order.order_status = orderStatus
            order.save()
            Payment.objects.create(address=address, contact_no=contactno, city=city, payment_type=payment_type, order=order, user=user)

            print("Successfully")
            return redirect("order-tables-user")

    print(order.total_price)     


    return render(request, 'customer/checkout.html', context)


@login_required(login_url='signup')
def order_tables_user(request):
    categories = Category.objects.all()
    context = {"categories":categories}
    
    if request.user.is_authenticated:
        user_email = request.user.email
        user = User.objects.get(email=request.user)
        # orders = Order.objects.filter(user=user)
        orderstatus_pending = OrderStatus.objects.get(order_status_type='pending')
        orders = Order.objects.filter(Q(user=user) & ~Q(order_status=orderstatus_pending))
        context["orders"] = orders
        total_items = 0

        # Iterate over each order and count the related order items
        for order in orders:
            orderitem = OrderItem.objects.filter(order=order).count()
            
            total_items += orderitem

        # Add the total count to the context
        context['qnt'] = total_items

        # Debugging output (optional)
        
        
    return render(request,'customer/order_statistic.html', context)

######################################### RECIPTIONIST/MANAGER #######################################

@restrict_customer
@login_required(login_url='signup')
def kitchen_home(request):
    if request.user.is_authenticated:
        manager = User.objects.get(email=request.user.email)
        inventories = Inventory.objects.all()
        print(inventories, manager)
        context = {"manager":manager, 'inventories':inventories}
    return render(request, 'manager/kitchen_home.html', context)

@restrict_customer
@login_required(login_url='signup')
def orders_kitchen(request):
    if request.user.is_authenticated:
        results = []
        manager = User.objects.get(email=request.user.email)
        orderStatus = OrderStatus.objects.get(order_status_type='pending')
        orders = Order.objects.filter(~Q(order_status=orderStatus)).order_by('-order_date')
        for order in orders:
            user = User.objects.get(email=order.user)
            orderItem_count = OrderItem.objects.filter(order=order).count()
            # print(order_count)
            payment = Payment.objects.filter(order=order, user=user)[0]
            # print(user, order, payment)
            results.append({
                "order":order,
                "payment":payment,
                "user":user,
                "order_menu_qnt": orderItem_count
            })
        context = {"manager":manager, "results":results}
    return render(request, 'manager/order_kitchen.html', context)

@restrict_customer
@login_required(login_url='signup')
def orders_detail(request, *args, **kwargs):
    if request.user.is_authenticated:
        manager = User.objects.get(email=request.user.email)  
        order_id = kwargs['order_id']
        user_id = kwargs['user_id']
        orderItems = OrderItem.objects.filter(order=Order.objects.get(id=order_id))
        context = {"manager":manager, "OrderItems": orderItems, "user":User.objects.get(id=user_id), 'order_id':order_id}
    return render(request, 'manager/order_detail.html', context)


def search_order_by_order_id(request):
    order_id = int(request.GET.get("order_id"))
    if Order.objects.filter(id = order_id).exists():
        
        order = Order.objects.filter(id = order_id)
        print(order_id, order)
        if Payment.objects.filter(order=order[0], user=User.objects.get(id=order[0].user.id)).exists():
            payment = Payment.objects.get(order=order[0], user=User.objects.get(id=order[0].user.id))
            
            order_details = [
                {
                    "order_id":ord.id,
                    "customer_id":ord.user.id,
                    "order_date":ord.order_date,
                    "order_status":ord.order_status.order_status_type,
                    "orderItem_qnt":OrderItem.objects.filter(order=ord).count()
                }
                for ord in order
            ]

            payment_detail = [
                {
                    "address":payment.address,
                    "contact_no":payment.contact_no
                }
            ]

            context = [
                {
                    "order":order_details,
                    "payment":payment_detail
                }
            ]


        
            return JsonResponse({'success': 'success', 'context': context})
        else:
            return JsonResponse({'error': 'This order ID is not placed Yet'})        
    return JsonResponse({'error': 'No Order by The Searched ID'})

def sort_by_btn(request):
    if request.user.is_authenticated:
        sort_type = request.GET.get('sort-type')
        if sort_type.lower().strip() == 'all':
            orderStatus = OrderStatus.objects.get(order_status_type='pending')
            orders = Order.objects.filter(~Q(order_status=orderStatus)).order_by('-order_date')
            if orders:
                results = []
                for order in orders: 
                    payment = Payment.objects.get(order=order)
                    results.append({
                        "order_id": order.id,
                        "customer_id": order.user.id,
                        "order_date": order.order_date,
                        "order_status": order.order_status.order_status_type,
                        "orderItem_qnt": order.orderitem_set.count(),
                        "payment": {
                            "address": payment.address,
                            "contact_no": payment.contact_no
                        }
                    })

                

                    
                
                return JsonResponse({"success":"success", "context":results})  
            return JsonResponse({'error': 'No Order'})
        
        
        orderStatus = OrderStatus.objects.get(order_status_type=sort_type.lower().strip())
        print(orderStatus)
        if Order.objects.filter(order_status=orderStatus).exists():
            orders = Order.objects.filter(order_status=orderStatus).order_by('-order_date')
            # payment = Payment.objects.get(order=orders)

            results = []
            for order in orders:
                payment = Payment.objects.get(order=order)
                results.append({
                    "order_id": order.id,
                    "customer_id": order.user.id,
                    "order_date": order.order_date,
                    "order_status": order.order_status.order_status_type,
                    "orderItem_qnt": order.orderitem_set.count(),
                    "payment": {
                        "address": payment.address,
                        "contact_no": payment.contact_no
                    }
                })

            

                
            
            return JsonResponse({"success":"success", "context":results})  
        return JsonResponse({'error': 'No Order'})

def Inventory_Restore(request):

    if request.user.is_authenticated:
        itm_inv = request.GET.get('item_inv')
        menu_item_id = request.GET.get('menu-item-id')
        menu = MenuItem.objects.get(id=menu_item_id)

        print(menu_item_id)


        if Inventory.objects.filter(menu=menu).exists():
            inventory = Inventory.objects.filter(menu=menu)[0]

            inventory.inventory_quantity = inventory.max_level_stock
            inventory.save()
            
            context = {
            "inventory_name": menu.menu_name,
            "inventory_quantity": inventory.inventory_quantity,
            "max_level_stock": inventory.max_level_stock,
            "min_level_stock": inventory.min_level_stock,
            }
            return JsonResponse({"success": "success", "context": context})
            
            

             
        else:
            return JsonResponse({"error": "Something Went Wrong!"})

    return JsonResponse({"success":"success"})

# def change_order_status(request):

#     order_id = request.GET.get('order-id')

#     if Order.objects.filter(id=order_id).exists():
        
#         orderStatus_completed = OrderStatus.objects.get(order_status_type='completed')
#         order_ = Order.objects.get(id = order_id)
#         order_.order_status = orderStatus_completed
#         order_.save()



#         results = []
#         orderStatus = OrderStatus.objects.get(order_status_type='pending')
#         orders = Order.objects.filter(~Q(order_status=orderStatus)).order_by('-order_date')
#         for order in orders:
#             print(order.order_status.order_status_type)
#             if order.id == order_id:
#                 print(order.order_status.order_status_type)

#             user = User.objects.get(email=order.user)
#             orderItem_count = OrderItem.objects.filter(order=order).count()
#             # print(order_count)
#             payment = Payment.objects.filter(order=order, user=user)[0]
#             # print(user, order, payment)
#             results.append({
#                 "order_id":order.id,
#                 "order_date":order.order_date,
#                 "order_status":order.order_status.order_status_type,
#                 "orderItem_count":OrderItem.objects.filter(order=order).count(),
#                 "customer_id":order.user.id,
#                 "address":payment.address,
#                 "contact_no":payment.contact_no,
#                 "user":user,
#                 "order_menu_qnt": orderItem_count
#             })
#         context = {"results":results}


#         return JsonResponse({"success":"success", "context":results})
#     else:
#         results = []
#         orderStatus = OrderStatus.objects.get(order_status_type='pending')
#         orders = Order.objects.filter(~Q(order_status=orderStatus)).order_by('-order_date')
#         for order in orders:
#             user = User.objects.get(email=order.user)
#             orderItem_count = OrderItem.objects.filter(order=order).count()
#             # print(order_count)
#             payment = Payment.objects.filter(order=order, user=user)[0]
#             # print(user, order, payment)
#             results.append({
#                 "order":order,
#                 "payment":payment,
#                 "user":user,
#                 "order_menu_qnt": orderItem_count
#             })
#         context = {"results":results}
#         return JsonResponse({"error":"Something Went Wrong", "context":results})

   
def change_order_status(request):
    order_id = request.GET.get('order-id')

    if not Order.objects.filter(id=order_id).exists():
        return JsonResponse({"error": "Order not found"})

    orderStatus_completed = OrderStatus.objects.get(order_status_type='completed')
    order_ = Order.objects.get(id=order_id)
    order_.order_status = orderStatus_completed
    order_.save()

    return get_order_context(request)

def get_order_context(request):
    results = []
    orderStatus_pending = OrderStatus.objects.get(order_status_type='pending')
    orders = Order.objects.filter(~Q(order_status=orderStatus_pending)).order_by('-order_date')
    
    for order in orders:
        user = order.user
        orderItem_count = OrderItem.objects.filter(order=order).count()
        payment = Payment.objects.filter(order=order, user=user).first()

        results.append({
            "order_id": order.id,
            "order_date": order.order_date,
            "order_status": order.order_status.order_status_type,
            "orderItem_count": orderItem_count,
            "customer_id": user.id,
            "address": payment.address if payment else "",
            "contact_no": payment.contact_no if payment else "",
            "user_email": user.email,
            "order_menu_qnt": orderItem_count
        })
    
    context = {"results": results}
    return JsonResponse({"success": "success", "context": results})