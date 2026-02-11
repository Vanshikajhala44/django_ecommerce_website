from django.shortcuts import render
from django.views import View
from .models import Cart, Product, OrderPlaced, Customer
from .forms import CustomerRegistrationForm
from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomerRegistrationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import UserProfileForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Address
from .forms import AddressForm





class Product_view(View):
    def get(self, request):
        if not request.user.is_authenticated:
         return redirect('login')
    
        topwears = Product.objects.filter(CATEGORY='TW')
        bottomwears = Product.objects.filter(CATEGORY='BW')
        mobiles = Product.objects.filter(CATEGORY='M')
        laptops = Product.objects.filter(CATEGORY='L')

        return render(request, 'app/home.html', {
            'topwears': topwears,
            'bottomwears': bottomwears,
            'mobiles': mobiles,
            'laptops': laptops,
        })


# ================= PRODUCT DETAIL =================
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product': product})



def product_filter(request, category, data=None):
    products = Product.objects.filter(CATEGORY=category)

    # 👉 Brand filter
    if data:
        products = products.filter(brand=data)

    # 👉 Price sorting
    sort = request.GET.get('sort')

    if sort == 'low':
        products = products.order_by('discounted_price')
    elif sort == 'high':
        products = products.order_by('-discounted_price')

    return render(request, 'app/product_list.html', {
        'products': products,
        'category': category,
        'brand': data
    })


@login_required
def buy_now(request):
    addresses = Address.objects.filter(user=request.user)  # get all addresses
    return render(request, 'app/buy_now.html', {'addresses': addresses})


@login_required
def profile(request):
    user = request.user
    profile = user.profile  # assumes you have a Profile model linked to User

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # reload page after save
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'app/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
from .forms import AddressForm

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address')  # redirect to address list page
    else:
        form = AddressForm()
    return render(request, 'app/add_address.html', {'form': form})


# ================= SIMPLE PAGES =================
def add_to_cart(request):
    return render(request, 'app/addtocart.html')


def buy_now(request):
    return render(request, 'app/buynow.html')


# def profile(request):
#     return render(request, 'app/profile.html')


# def address(request):
#     return render(request, 'app/address.html')


def orders(request):
    return render(request, 'app/orders.html')


def change_password(request):
    return render(request, 'app/changepassword.html')

def password_change_done(request):
    return render(request, 'app/password_change_done.html')



def login(request):
    return render(request, 'app/login.html')

def logout_function(request):
    logout(request)  
    return redirect('login')




class CustomerRegistrationView(View):

    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')   # ya home page

        # agar form invalid ho
        return render(request, 'app/customerregistration.html', {'form': form})


def checkout(request):
    return render(request, 'app/checkout.html')

