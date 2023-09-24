from core.models import Product, Category, Vendor, CartOrderItems, CartOrder, ProductImages, ProductReview, wishlist, Address
from userauths.models import User

def default(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:
            address = None
    else:
        address = None
    user = User.objects.all()

    return {
        "categories":categories,
        "user":user,
        "address":address
    }