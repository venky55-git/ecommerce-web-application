# In shop/context_processors.py

from .models import Wishlist, Cart


def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        return {'wishlist_count': wishlist.products.count()}
    return {'wishlist_count': 0}

def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {'cart_count': cart.items.count()}
        except Cart.DoesNotExist:
            return {'cart_count': 0}
    return {'cart_count': 0}