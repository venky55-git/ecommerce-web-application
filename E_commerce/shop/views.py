from django.conf import settings  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignupForm, ProductForm
from django.conf import settings  
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignupForm, ProductForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db.models import Sum 

  #views for the deshboard
from django.http import JsonResponse
from datetime import datetime, timedelta

# project a
from django.utils import timezone
from datetime import timedelta
from .models import Product, Cart, CartItem, Wishlist, Order, ProductReview
from .forms import ReviewForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import CustomerAddress, Payment, Order, Wishlist
from .forms import AddressForm, PaymentMethodForm
from .forms import UserProfileForm, AddressForm
import logging

logger = logging.getLogger(__name__)


 








def is_admin(user):
    return user.is_superuser

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save()

            # Log the user in after successful registration
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
            
            return redirect('home')  # Redirect to homepage or a specific page after successful signup
    else:
        form = SignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})


@user_passes_test(is_admin)  
def admin_dashboard(request):
    products = Product.objects.all()
    orders = Order.objects.filter(status='Pending')

    # Count total quantity of delivered orders (each item sold counts)
    from django.db.models import Sum
    delivered_cartitem_ids = (
        Order.objects.filter(status='D')
        .values_list('items', flat=True)
    )
    total_sales = CartItem.objects.filter(id__in=delivered_cartitem_ids).aggregate(total=Sum('quantity'))['total'] or 0

    # Count all active non-superuser users
    active_users = User.objects.filter(is_superuser=False, is_active=True).count()

    # Fetch recent product reviews (latest 5)
    recent_reviews = ProductReview.objects.select_related('product', 'user').order_by('-created_at')[:5]

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm()

    return render(request, 'shop/admin_dashboard.html', {
        'form': form,
        'products': products,
        'orders': orders,
        'total_sales': total_sales,
        'active_users': active_users,
        'recent_reviews': recent_reviews,
    })
def sales_report_view(request):
    # Placeholder for sales report page
    return render(request, 'shop/sales_report.html')

def pending_orders(request):
    # Show all orders with status 'Pending'
    orders = Order.objects.filter(status='P')
    return render(request, 'shop/pending_order.html', {'orders': orders})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_dashboard')

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})

def approve_order(request, order_id):
    if not request.user.is_superuser:
        return redirect('login')
    order = get_object_or_404(Order, id=order_id)
    order.status = 'PR'  # Processing/Approved
    order.save()
    messages.success(request, f"Order #{order.id} approved.")
    return redirect('pending_orders')

def reject_order(request, order_id):
    if not request.user.is_superuser:
        return redirect('login')
    order = get_object_or_404(Order, id=order_id)
    order.status = 'C'  # Cancelled
    order.save()
    messages.success(request, f"Order #{order.id} rejected.")
    return redirect('pending_orders')

def sales_report_view(request):
    # Aggregate total units sold for each product
    report = (
        CartItem.objects
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')
    )
    return render(request, 'shop/sales_report.html', {'report': report})        



def home(request):
    products = Product.objects.all()
    category = request.GET.get('category')
    search = request.GET.get('search')

    if category:
        products = products.filter(category=category)
    if search:
        products = products.filter(name__icontains=search)

    categories = Product.CATEGORY_CHOICES  # Make sure this matches your model
    
    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
    })

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('admin_dashboard')
        else:
            return reverse_lazy('my_account')
        



# filepath: c:\E-commerce project\E_commerce\shop\views.py



    
    
    
    
    
    
    
    
    

# project a-------------------------------------------------------------------------------------------------------->
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })
    
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} added to cart")
    return redirect('cart')

@login_required
def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    context = {
        'cart': cart,
        'total_price': sum(item.total_price for item in cart.items.all())
    }
    return render(request, 'shop/cart.html', context)

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(
            id=item_id,
            cart__user=request.user  # Ensure the item belongs to the user's cart
        )
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f"{product_name} removed from cart")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in your cart")
    return redirect('cart')


@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'shop/wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    
    if product not in wishlist.products.all():
        wishlist.products.add(product)
        messages.success(request, f"{product.name} added to wishlist")
    else:
        messages.info(request, f"{product.name} is already in your wishlist")
    
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        estimated_delivery = timezone.now().date() + timedelta(days=7)
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price,
            shipping_address=request.POST.get('shipping_address', ''),
            estimated_delivery=estimated_delivery
        )
        
        for item in cart.items.all():
            order.items.add(item)
        
        cart.items.all().delete()
        
        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'shop/checkout_address.html', {'cart': cart})

#@login_required
#def order_review(request, order_id):
    #order = get_object_or_404(Order, id=order_id, user=request.user)
   #return render(request, 'shop/order_review.html', {'order': order})






@login_required
def checkout_address(request):
    cart = get_object_or_404(Cart, user=request.user)
    addresses = CustomerAddress.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('checkout_payment')
    else:
        form = AddressForm()
    
    return render(request, 'shop/checkout_address.html', {
        'cart': cart,
        'addresses': addresses,
        'form': form
    })

@login_required
def checkout_payment(request):
    cart = get_object_or_404(Cart, user=request.user)
    default_address = CustomerAddress.objects.filter(user=request.user, is_default=True).first()
    
    if not default_address:
        messages.error(request, "Please add a shipping address first")
        return redirect('checkout_address')
    
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            
            if payment_method == 'COD':
                return process_cod_payment(request, cart, default_address)
            
    
    
    return render(request, 'shop/checkout_payment.html', {
        'cart': cart,
        'address': default_address,
        
    })

def process_cod_payment(request, cart, address):
    # Create order
    estimated_delivery = timezone.now().date() + timedelta(days=7)
    order = Order.objects.create(
        user=request.user,
        total_price=cart.total_price,
        shipping_address=str(address),
        status='PR',  # processing
        estimated_delivery=estimated_delivery
    )
    
    # Add items to order
    for item in cart.items.all():
        order.items.add(item)
    
    
    
    # Clear cart
    cart.items.all().delete()
    
    # Send confirmation email
    send_order_confirmation(request, order)
    
    return redirect('order_confirmation', order_id=order.id)



def send_order_confirmation(request, order):
    # Render invoice HTML
    invoice_html = render_to_string('shop/invoice_template.html', {
        'order': order,
        'user': request.user
    })
    
    # Create PDF (requires reportlab or other PDF library)
    #pdf = generate_pdf(invoice_html)  # Implement this function
    
    # Send email
    subject = f"Order Confirmation #{order.id}"
    message = f"Thank you for your order! Your order ID is #{order.id}"
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email]
    )
    #email.attach(f'invoice_{order.id}.pdf', pdf, 'application/pdf')
    
    email.send()
   # generate pdf python weasyprint----------------------------------------------->
    
   

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment = Payment.objects.filter(order=order).first()
    
    return render(request, 'shop/order_confirmation.html', {
        'order': order,
        'payment': payment
    })

@login_required
def view_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/invoice_template.html', {
        'order': order,
        'user': request.user
    })

@login_required
def checkout_payment(request):
    cart = get_object_or_404(Cart, user=request.user)
    default_address = CustomerAddress.objects.filter(user=request.user, is_default=True).first()
    
    if not default_address:
        messages.error(request, "Please add a shipping address first")
        return redirect('checkout_address')
    
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            
            if payment_method == 'COD':
                return process_cod_payment(request, cart, default_address)
            # Remove Razorpay condition
    else:
        form = PaymentMethodForm()
    
    return render(request, 'shop/checkout_payment.html', {
        'cart': cart,
        'address': default_address,
        'form': form,
        # Remove razorpay_key from context
    })
    
    
    
    
    
    
    
    
    # my account section----------------------------------------------------------------------------->
# shop/views.py
@login_required
def my_account(request):
    default_address = request.user.customeraddress_set.filter(is_default=True).first()
    return render(request, 'shop/account/my_account.html', {
        'default_address': default_address
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('my_account')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'shop/account/edit_profile.html', {'form': form})

@login_required
def address_list(request):
    addresses = CustomerAddress.objects.filter(user=request.user)
    return render(request, 'shop/account/address_list.html', {'addresses': addresses})


@login_required
def edit_address(request, address_id):
    address = get_object_or_404(CustomerAddress, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully!")
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'edit_address.html', {'form': form})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(CustomerAddress, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, "Address deleted successfully!")
    return redirect('address_list')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/account/order_history.html', {'orders': orders})    

@login_required
def my_orders_view(request):
    my_orders = Order.objects.filter(user=request.user).select_related('product')
    return render(request, 'shop/account/order_history.html', {'my_orders': my_orders})


# Admin view for all orders
@user_passes_test(is_admin)
def all_orders_view(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    return render(request, 'shop/account/all_orders.html', {'orders': orders})


#@login_required
#def my_orders(request):
   # orders = Order.objects.filter(user=request.user).select_related('product')
   # return render(request, 'order_history.html', {'orders': orders})


#place_order section------------------------------------------------------->
@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        # Process the order
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=1,  # Default quantity
            total_price=product.price,
            shipping_address=request.user.customeraddress_set.filter(is_default=True).first(),
            status='P'  # Pending
        )
        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation', order_id=order.id)
    
    # Default address for the order
    default_address = request.user.customeraddress_set.filter(is_default=True).first()
    
    return render(request, 'shop/place_order.html', {
        'product': product,
        'default_address': default_address
    })
    
# add adress section ---------------------->
@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            
            # If setting as default, remove default from others
            if form.cleaned_data['is_default']:
                CustomerAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
            
            address.save()
            messages.success(request, "Address added successfully!")
            return redirect('address_list')
    else:
        form = AddressForm()
    
    return render(request, 'shop/account/add_address.html', {'form': form})    

@login_required
def view_invoice(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('order_history')
    return render(request, 'shop/invoice_template.html', {
        'order': order,
        'user': request.user
    })
    
    
from django.core.paginator import Paginator
from django.shortcuts import render

def all_orders_view(request):
    orders_list = Order.objects.all().order_by('-created_at')  # or your preferred ordering
    paginator = Paginator(orders_list, 10)  # Show 10 orders per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,  # Use page_obj as orders in your template
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'shop/account/all_orders.html', context)



from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Order

def order_history_view(request):
    orders_list = Order.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(orders_list, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'orders': page_obj,  # Use page_obj for iteration in template
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    return render(request, 'shop/account/order_history.html', context)

def fashion_view(request):
    # Get all fashion-related products
    products = Product.objects.filter(
        category__in=['Fashions', 'Men', 'Women', 'Kids', 'Footwear']
    )
    
    # Apply filters
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    
    price_range = request.GET.get('price')
    if price_range:
        if price_range == '0-500':
            products = products.filter(price__lte=500)
        elif price_range == '500-1000':
            products = products.filter(price__gt=500, price__lte=1000)
        elif price_range == '1000-2000':
            products = products.filter(price__gt=1000, price__lte=2000)
        elif price_range == '2000':
            products = products.filter(price__gt=2000)
    
    size = request.GET.get('size')
    if size:
        products = products.filter(size=size)
    
    color = request.GET.get('color')
    if color:
        products = products.filter(color=color)
    
    # Get unique sizes and colors for filters
    sizes = Product.objects.filter(
        category__in=['Fashions', 'Men', 'Women', 'Kids', 'Footwear']
    ).exclude(size__isnull=True).values_list('size', flat=True).distinct()
    
    colors = Product.objects.filter(
        category__in=['Fashions', 'Men', 'Women', 'Kids', 'Footwear']
    ).exclude(color__isnull=True).values_list('color', flat=True).distinct()
    
    return render(request, 'shop/fashion.html', {
        'products': products,
        'sizes': sizes,
        'colors': colors,
    })
    
    
    # mobile section-------------------------------------------------------------->


def electronics_page(request):
    electronics_products = Product.objects.filter(category__in=['mobile', 'watch', 'fridge', 'fan', 'tv', 'ac'])
    
    # Apply filters if they exist
    category = request.GET.get('category')
    if category and category != 'all':
        electronics_products = electronics_products.filter(category=category)
    
    price_filter = request.GET.get('price')
    if price_filter == 'under5000':
        electronics_products = electronics_products.filter(price__lt=5000)
    elif price_filter == '5000-10000':
        electronics_products = electronics_products.filter(price__gte=5000, price__lte=10000)
    elif price_filter == '10000-20000':
        electronics_products = electronics_products.filter(price__gte=10000, price__lte=20000)
    elif price_filter == 'above20000':
        electronics_products = electronics_products.filter(price__gt=20000)
    
    return render(request, 'shop/mobile.html', {
        'electronics_products': electronics_products
    })