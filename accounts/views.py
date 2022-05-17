from mimetypes import init
from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import CustomerForm, OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import admin_only, allowed_users, unauthanticated_user

@unauthanticated_user
# register sayfası
def registerPage(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,"Your account has been created successfully -" + username)
            return redirect('loginurl')

    context = {"form": form}
    return render(request,"accounts/register.html",context)

@unauthanticated_user
# login sayfası
def loginPage(request):
    if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect("homeurl")
            else:
                messages.info(request,"Username or Password incorrect!")

    context = {}
    return render(request,"accounts/login.html",context)

# logout fonksiyonu
def logoutUser(request):
    logout(request)
    return redirect('loginurl')

@login_required(login_url="loginurl")
@admin_only
#anasayfa
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    total_delivered = orders.filter(status="delivered").count()
    total_pending = orders.filter(status="pending").count()

    total_customers = customers.count()

    context = {
        "orders":orders,
        "customers":customers,
        "total_orders":total_orders,
        "total_delivered":total_delivered,
        "total_pending":total_pending,
        "total_customers":total_customers
    }
    return render(request,"accounts/dashboard.html",context)

@login_required(login_url="loginurl")
@allowed_users(allowed_roles=["admin"])
# product sayfası
def product(request):
    products = Product.objects.all()

    return render(request,"accounts/profile.html", {"products":products})

@login_required(login_url="loginurl")
@allowed_users(allowed_roles=["admin"])
# cutomer sayfası 
def customer(request,pk_customer):
    customer = Customer.objects.get(id=pk_customer)
    orders = customer.order_set.all()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    return render(request,"accounts/customer.html",{"customer": customer,"orders":orders,"myFilter":myFilter})

@login_required(login_url="loginurl")
@allowed_users(allowed_roles=["customer"])
# user sayfası
def userPage(request):
    orders = request.user.customer.order_set.all()  
    total_orders = orders.count()
    total_delivered = orders.filter(status="delivered").count()
    total_pending = orders.filter(status="pending").count()
    context = {"orders":orders,"total_orders":total_orders,"total_delivered":total_delivered,"total_pending":total_pending}
    return render(request,"accounts/user.html",context)

@login_required(login_url="loginurl")
@allowed_users(allowed_roles=["admin"])
#oluşturna fonksiyonu
def create_order(request,pk_customer):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=("product","status"),extra=10)

    customer = Customer.objects.get(id=pk_customer)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)

    # formset ile değiştirdim
    # tek satırlık form işlemi
    #form = OrderForm(initial={"customer": customer})

    if request.method == "POST":
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("/")
    # form değişkenini formset ile değiştirdim
    context = {"formset": formset,"customer": customer}
    return render(request,"accounts/order_form.html",context)

@login_required(login_url="loginurl")
@allowed_users(allowed_roles=["admin"])
#güncelleme fonksiyonu
def update_order(request,pk_order):
    order = Order.objects.get(id=pk_order)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form= OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"form": form}
    return render(request,"accounts/order_form.html",context)

@login_required(login_url="loginurl")
@allowed_users(allowed_roles=["admin"])
# silme fonksiyonu
def delete_order(request,pk_order):
    order = Order.objects.get(id=pk_order)
    if request.method == "POST":
        order.delete()
        return redirect("/")

    context = {"item": order}
    return render(request,"accounts/delete_order.html",context)

# hesap ayarları fonksiyonu
def account_set(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request,"accounts/account_settings.html",context)
