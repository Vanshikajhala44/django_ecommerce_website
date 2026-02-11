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
from .models import Product, Cart, Address, Order
from django.shortcuts import get_object_or_404, redirect







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


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
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
    addresses = Address.objects.filter(user=user)  # get all addresses

    if request.method == "POST":
        # check which form is submitted
        if 'update_profile' in request.POST:
            user_form = UserProfileForm(request.POST, instance=user)
            profile_form = ProfileForm(request.POST, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('profile')
        elif 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                address.save()
                return redirect('profile')
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        address_form = AddressForm()

    return render(request, 'app/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': address_form,
        'addresses': addresses
    })
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

@login_required
def edit_address(request, id):
    # Get the address for the logged-in user
    address = Address.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        # Pass the instance to pre-fill the form
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address')  # After saving, go back to address list
    else:
        form = AddressForm(instance=address)  # Pre-fill form with existing data

    # Render the same template as add_address
    return render(request, 'app/add_address.html', {'form': form})

@login_required
def delete_address(request, id):
    address = Address.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        address.delete()
        return redirect('address')
    return render(request, 'app/delete_address.html', {'address': address})




@login_required
def address(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'addresses': addresses})

# ================= SIMPLE PAGES =================
# def add_to_cart(request):
#     return render(request, 'app/addtocart.html')


def buy_now(request):
    return render(request, 'app/buynow.html')





@login_required
def add_to_cart(request):
    product_id = request.GET.get('prod_id')

    if not product_id:
        return redirect('cart')

    product = get_object_or_404(Product, id=product_id)

    Cart.objects.create(
        user=request.user,
        product=product
    )

    return redirect('cart')


def show_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        amount = sum(item.total_cost for item in cart)
        totalamount = amount + 40

        return render(request, 'app/cart.html', {
            'cart': cart,
            'amount': amount,
            'totalamount': totalamount,
        })
    else:
        return redirect('login')


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)

    amount = sum(item.total_cost for item in cart)
    shipping = 40
    total_amount = amount + shipping

    return render(request, 'app/checkout.html', {
        'cart': cart,
        'addresses': addresses,
        'amount': amount,
        'shipping': shipping,
        'total_amount': total_amount
    })

@login_required
def place_order(request):
    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = Address.objects.get(id=address_id)
        cart_items = Cart.objects.filter(user=request.user)

        for item in cart_items:
            Order.objects.create(
                user=request.user,
                address=address,
                product=item.product,
                quantity=item.quantity
            )

        cart_items.delete()
        return redirect('order_success')

def order_success(request):
    return render(request, 'app/order_success.html')



# def profile(request):
#     return render(request, 'app/profile.html')


# def address(request):
#     return render(request, 'app/address.html')


# def orders(request):
#     return render(request, 'app/orders.html')


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

