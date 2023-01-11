from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages

# Imported from project
from .models import *
from .forms import *
from .filters import OrderFilter
from .decorators import unauthenticated_user,allowed_users,admin_only

@unauthenticated_user
def registerPage(request):
    
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            

            messages.success(request,'Account was created for ' + username)
            return redirect('login')

    context = {'form':form}

    return render(request,'my_crm/register.html',context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect.')

    context = {}

    return render(request,'my_crm/login.html',context)

def logoutUser(request): 
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for Delivery').count()

    context = {
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'out_for_delivery':out_for_delivery,
    }

    return render(request,'my_crm/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            

    context = {'form':form}
    return render(request,'my_crm/account_settings.html',context)

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for Delivery').count()

    context = {
        'customers':customers,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'out_for_delivery':out_for_delivery,
    }
    return render(request,'my_crm/home.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request,'my_crm/products.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    orders_count = orders.count()    

    context = {'customer':customer, 'orders':orders,'orders_count':orders_count, 'myFilter':myFilter}

    return render(request,'my_crm/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def order(request):
    customer = Customer.objects.all()
    orders = Order.objects.all()
    products = Product.objects.all()
    context = {'customer':customer, 'orders':orders, 'products':products}
    return render(request,'my_crm/orders.html',context)


# CRUD Operations
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)

    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer':customer})
    # Saving the form values 
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/orders')

    context = {'formset':formset}
    return render(request, 'my_crm/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid:
            form.save()
            return redirect('/orders')
    context = {'form':form}
    return render(request, 'my_crm/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/orders')

    context = {'item':order}
    
    return render(request,'my_crm/delete.html',context)
