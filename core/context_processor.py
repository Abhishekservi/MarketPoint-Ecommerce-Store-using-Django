from core.models import Product, Category, Vendor, CartOrderItems, CartOrder, ProductImages, ProductReview, wishlist, Address


def default(request):
    categories = Category.objects.all()



    return {
        "categories":categories
    }