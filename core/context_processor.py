from core.models import Product, Category, Vendor, CartOrderItems, CartOrder, ProductImages, ProductReview, wishlist_model, Address
from userauths.models import User
from django.db.models import Count, Max, Min
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    cart_total_amount = 0
    delivery_total_cost = 0 
    totol_amount = 0

    if request.user.is_authenticated:

        try:
        # Calculate cart total
            if 'cart_data_obj' in request.session:
                    for p_id, item in request.session['cart_data_obj'].items():
                        cart_total_amount+=int(item['qty'])*float(item['price'])
            
        except:
            # Handle any errors
            pass

    # Calculate delivery cost
    if cart_total_amount >= 1000:  
        delivery_total_cost = cart_total_amount
    else:
        delivery_total_cost = cart_total_amount + 100
    
    if cart_total_amount < 500:
        delivery = 0
    else:
        delivery = 1


    try:
        wishlist = wishlist_model.objects.filter(user=request.user)
    except:
        # messages.warning(request, "You need to login before accesing the wishlist.")
        wishlist=0

    if request.user.is_authenticated:
        try:
            address = Address.objects.filter(user=request.user)
        except Address.DoesNotExist:
            address = None
    else:
        address = None
    user = User.objects.all()
    

    return {
        "categories":categories,
        "wishlist":wishlist,
        "user":user,
        "address":address,
        "vendors":vendors,
        # "min_max_price":min_max_price,
        "delivery_total_cost":delivery_total_cost,
        "delivery":delivery,
    }