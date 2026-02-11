from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views
from django.views.generic import TemplateView




urlpatterns = [

    # Home
    path('', views.Product_view.as_view(), name='home'),

    # Product detail
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # Cart & user
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    # path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),

    # Auth
    path('login/', views.login, name='login'),
   path(
    'registration/',
    views.CustomerRegistrationView.as_view(),
    name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),

    path('mobile/', views.product_filter, {'category': 'M'}, name='mobiles'),
    path('mobile/<slug:data>/', views.product_filter, {'category': 'M'}, name='mobiledata'),
    


    path('topwear/', views.product_filter, {'category': 'TW'}, name='topwear'),
    path('topwear/<slug:data>/', views.product_filter, {'category': 'TW'}, name='topweardata'),

   
    path('bottomwear/', views.product_filter, {'category': 'BW'}, name='bottomwear'),
    path('bottomwear/<slug:data>/', views.product_filter, {'category': 'BW'}, name='bottomweardata'),


    path('laptop/', views.product_filter, {'category': 'L'}, name='laptops'),
    path('laptop/<slug:data>/', views.product_filter, {'category': 'L'}, name='laptopdata'),
   path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='app/login.html',
            authentication_form=LoginForm), name='login'),
 

   path('logout/', views.logout_function, name='logout'),
  path('change-password/', 
         auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html' ,success_url="/change-password/done/"), 
         name='changepassword'),
    path('change-password/done/', 
         TemplateView.as_view(template_name='app/password_change_done.html'), 
         name='password_change_done'),
    # path('change-password/done/', views.password_change_done, name='password_change_done'),=
    # path('change-password/', views.change_password, name='changepassword'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
