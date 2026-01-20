
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# project a
from .views import (
    checkout_address, checkout_payment, order_confirmation, 
    view_invoice, 
)

urlpatterns = [
    #path('api/sales-data/', views.sales_data_api, name='sales_data_api'),
    path('approve-order/<int:order_id>/', views.approve_order, name='approve_order'),
    path('reject-order/<int:order_id>/', views.reject_order, name='reject_order'),
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    #path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('signup', views.signup_view, name='signup'),
    path('accounts/login', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('all-orders/', views.all_orders_view, name='all_orders_view'),
    path('pending-orders/', views.pending_orders, name='pending_orders'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('sales-report/', views.sales_report_view, name='sales_report'),
    #path('my-orders/', views.my_orders, name='my_orders'),
    path('place-order/<int:product_id>/', views.place_order, name='place_order'),
    path('fashion/', views.fashion_view, name='fashion'),
    
    
    # project a
     path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    #path('order-review/<int:order_id>/', views.order_review, name='order_review'),
    
    path('checkout/address/', checkout_address, name='checkout_address'),
    path('checkout/payment/', checkout_payment, name='checkout_payment'),
    path('order/confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('order/invoice/<int:order_id>/', view_invoice, name='view_invoice'),
    
    #my account section
     path('my-account/', views.my_account, name='my_account'),
    path('my-account/edit-profile/', views.edit_profile, name='edit_profile'),
    path('my-account/addresses/', views.address_list, name='address_list'),
    path('my-account/addresses/add/', views.add_address, name='add_address'),
    path('my-account/addresses/edit/<int:address_id>/', views.edit_address, name='edit_address'),
    path('my-account/addresses/delete/<int:address_id>/', views.delete_address, name='delete_address'),
    path('my-account/orders/', views.order_history_view, name='order_history'),
    path('my-account/wishlist/', views.wishlist, name='wishlist'),
    path('electronics/', views.electronics_page, name='electronics'),
]


