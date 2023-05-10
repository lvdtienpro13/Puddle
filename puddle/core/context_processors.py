from .models import Profile
from item.models import OrderItem, Order

def profile_picture(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return {'profile_picture': profile.profileimg.url}
        except Profile.DoesNotExist:
            pass
    return {}

def cart_item_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(user=request.user, ordered=False)
        cart_count = order_items.count()
    return {'cart_item_count': cart_count}