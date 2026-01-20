
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # project a
from django.core.validators import MinValueValidator, MaxValueValidator # project a
from datetime import timedelta
from django.utils.text import slugify



class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Mobiles', 'Mobiles'),
        ('Watches', 'Watches'),
        ('Smartwatches', 'Smartwatches'),
        ('Laptops', 'Laptops'),
        ('Electronics', 'Electronics Gadgets'),
        ('Fashions', 'Fashions'),
        ('Men', 'Men Fashion'),
        ('Women', 'Women Fashion'),
        ('Kids', 'Kids Fashion'),
        ('Footwear', 'Footwear'),
    ]
    
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
        ('28', '28'),
        ('30', '30'),
        ('32', '32'),
        ('34', '34'),
        ('36', '36'),
        ('38', '38'),
        ('40', '40'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]
    
    COLOR_CHOICES = [
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Black', 'Black'),
        ('White', 'White'),
        ('Yellow', 'Yellow'),
        ('Pink', 'Pink'),
        ('Purple', 'Purple'),
        ('Gray', 'Gray'),
        ('Brown', 'Brown'),
    ]
    
    # Existing fields
    name = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    # New fashion-specific fields
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# project a

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s review for {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"

class Wishlist(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='wishlist' )
    products = models.ManyToManyField('shop.Product', related_name='wishlists')
    
    def __str__(self):
        return f"Wishlist of {self.user.username}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('PR', 'Processing'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2 ,default=0 )
    shipping_address = models.TextField(
        default="Address not provided",  # Or any sensible defaul
        blank=True  # Also add this if the field can be empty
        )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PR')
    created_at = models.DateTimeField(auto_now_add=True)
    estimated_delivery = models.DateField(
        default=timezone.now() + timedelta(days=7)  # Default to 7 days from now
    )
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class CustomerAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=20, choices=[('HOME', 'Home'), ('WORK', 'Work')])
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_address_type_display()} - {self.street}, {self.city}"

class Payment(models.Model):
     PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        # Remove Razorpay option:
        # ('RAZORPAY', 'Razorpay'),
    ]
     order = models.ForeignKey(Order, on_delete=models.CASCADE)
     payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default='COD'
        )
     transaction_id = models.CharField(max_length=100)
     amount = models.DecimalField(max_digits=10, decimal_places=2)
     status = models.CharField(max_length=20)
     created_at = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
        return f"Payment #{self.id} for Order {self.order.id}"

