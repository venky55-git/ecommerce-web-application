
from django.contrib import admin
from .models import Product, Cart, CartItem, Wishlist, Order, ProductReview, CustomerAddress, Payment

class CartItemInline(admin.TabularInline):
    model = Order.items.through
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_names', 'product_quantities', 'total_price', 'status', 'created_at', 'estimated_delivery', 'total_sales')
    def product_names(self, obj):
        return ", ".join([item.product.name for item in obj.items.all()])
    product_names.short_description = 'Products'

    def product_quantities(self, obj):
        return ", ".join([str(item.quantity) for item in obj.items.all()])
    product_quantities.short_description = 'Quantities'
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    readonly_fields = ('created_at', 'estimated_delivery')
    inlines = [CartItemInline]

    def total_sales(self, obj):
        from .models import Order
        return Order.objects.aggregate(total_sales=admin.models.Sum('total_price'))['total_sales'] or 0
    total_sales.short_description = 'Total Sales (All Orders)'

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username')

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(CustomerAddress)
admin.site.register(Payment)

