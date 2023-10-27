from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.db.models import Count,Avg,Q

from core.models import Product, Category, Vendor, CartOrderItems, CartOrder, ProductImages, ProductReview, Address, wishlist_model
from userauths.models import ContactUs
from taggit.models import Tag
from core.forms import ProductReviewForm    
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.geolocation_utils import geocode_address

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import razorpay

from django.core import serializers

import calendar
from django.db.models.functions import ExtractMonth

# Create your views here.
def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured=True).order_by("-id")
    topselling = Product.objects.filter(product_status="published", featured=True).order_by("-id")[3:6]
    recently_added = Product.objects.filter(product_status="published", featured=True).order_by("-id")[:3]
    context={
        "products":products,
        "recently_added":recently_added,
        "topsel":topselling,
        
    }
    return render(request, "core/index.html",context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published").order_by("-id")
    
    context={
        "products":products,
        
    }
    return render(request, "core/product-list.html",context)


def category_list_view(request):

    categories = Category.objects.all()
    # categories = Category.objects.all().annotate(product_count=Count("products"))
    

    context ={
        "categories":categories,
        
    }

    return render(request,'core/category-list.html',context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)

    

    context = {
        "category":category,
        "products":products,
    }

    return render(request,"core/category-product-list.html", context)


def vendor_list_view(request):
    vendor = Vendor.objects.all()
    
    context = {
        "vendor":vendor,
        
    }

    return render(request, "core/vendors-list.html", context)


def vendor_detail_view(request,vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")
    
    context = {
        "vendor":vendor,
        "products":products,
        

    }

    return render(request, "core/vendor-detail.html", context)

def product_detail_view(request,pid):
    product = Product.objects.get(pid=pid)

    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    #Getting the reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    #Getting average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    avg_rating = average_rating['rating']
    try:
        rating_percent = avg_rating*20
    except:
        rating_percent = 0
    #Product Review Form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    p_image = product.p_images.all()
    
    context ={
        "P":product,
        "make_review":make_review,
        "p_image":p_image,
        "products":products,
        "reviews":reviews,
        "average_rating":average_rating,
        "review_form":review_form,
        "rating_percent":rating_percent,
        
    }
    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug = None):

    products = Product.objects.filter(product_status="published").order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context ={
        "products":products,
        "tag":tag   
    }

    return render(request, "core/tag.html", context)

def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid) 
    user=request.user   

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
        
    )
    
    context = {
        'user': user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],

    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
         'bool':True,
         'context':context,
         'average_reviews':average_reviews,
        }
    )
        

def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date") # Amul Tazza > Amul or ul or am

    context = {
        "products":products,
        "query":query,
    }
    return render(request, "core/search.html", context)


def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    try:
        products = products.filter(price__gte=min_price)
    except:
        products = products.filter(price__gte=18)
    try:
        products = products.filter(price__lte=max_price)
    except:
        products = products.filter(price__lte=530)    
    

    if len(categories)>0:
        products = products.filter(category__id__in=categories).distinct() 
    
    if len(vendors)>0:
        products = products.filter(vendor__id__in=vendors).distinct()

    data = render_to_string("core/async/product-list.html",{"products":products})
    return JsonResponse({"data": data})

def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

 
def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount+=int(item['qty'])*float(item['price'])

        if cart_total_amount>=1000:
            shipping_cost=0
            delivery_total_cost = cart_total_amount
        else:
            shipping_cost=100
            delivery_total_cost = cart_total_amount+shipping_cost
        if cart_total_amount<500:
            delivery=0
        else:
            delivery=1

        return render(request, "core/cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, 'shipping_cost':shipping_cost, "delivery":delivery, "delivery_total_cost":delivery_total_cost})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")
    
def delete_item(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount+=int(item['qty'])*float(item['price'])

        if cart_total_amount>=1000:
            shipping_cost=0
            delivery_total_cost = cart_total_amount
        else:
            shipping_cost=100
            delivery_total_cost = cart_total_amount+shipping_cost
        if cart_total_amount<500:
            delivery=0
        else:
            delivery=1
    
    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, 'shipping_cost':shipping_cost, "delivery":delivery, "delivery_total_cost":delivery_total_cost})

    return JsonResponse({"data":context,'totalcartitems': len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_quantity = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_quantity
            request.session['cart_data_obj'] = cart_data
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount+=int(item['qty'])*float(item['price'])

        if cart_total_amount>=1000:
            shipping_cost=0
            delivery_total_cost = cart_total_amount
        else:
            shipping_cost=100
            delivery_total_cost = cart_total_amount+shipping_cost
        if cart_total_amount<500:
            delivery=0
        else:
            delivery=1
    
    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, 'shipping_cost':shipping_cost, "delivery":delivery, "delivery_total_cost":delivery_total_cost})

    return JsonResponse({"data":context,'totalcartitems': len(request.session['cart_data_obj'])})

def clear_cart(request):

    # Clear the cart session data
    del request.session['cart_data_obj']
    
    return JsonResponse({'success': True})

@login_required 
@csrf_exempt
def checkout_view(request):

    cart_total_amount = 0
    totol_amount = 0
    if 'cart_data_obj' in request.session:

        #Getting total amount for Payment
        for p_id, item in request.session['cart_data_obj'].items():
            totol_amount += int(item['qty'])*float(item['price'])

        if totol_amount>=1000:
            shipping_cost=0
            delivery_total_cost = totol_amount
        else:
            shipping_cost=100
            delivery_total_cost = totol_amount+shipping_cost
        if totol_amount<500:
            delivery=0
        else:
            delivery=1


        order = CartOrder.objects.create(
            user = request.user,
            price = delivery_total_cost,
        )

        #Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty'])*float(item['price'])

            cart_order_products = CartOrderItems.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id), #Invoice_NO-3
                item = item['title'],
                image = item['image'],
                qty = item['qty'],
                price = item['price'],
                total = float(item['qty'])*float(item['price'])
            )

    client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID , settings.SECRET_KEY))

     # Create a Razorpay order
    order_amount = delivery_total_cost*100  # Replace with your desired amount in paise (e.g., 1000 = ₹10.00)
    order_currency = 'INR'
    order_receipt = 'INVOICE_NO-" + str(order.id),'  # Replace with your order receipt identifier

    order = client.order.create({
        'amount': order_amount,
        'currency': order_currency,
        'receipt': order_receipt,
    })

    # Get the success and failure redirect URLs from the URL parameters or set defaults
    success_redirect_url = request.GET.get('success_redirect_url', 'payment-completed/')
    failure_redirect_url = request.GET.get('failure_redirect_url', 'payment-failed/')

    # Construct the complete success and failure redirect URLs
    full_success_redirect_url = request.build_absolute_uri(success_redirect_url)
    full_failure_redirect_url = request.build_absolute_uri(failure_redirect_url)


    try:    
        active_address = Address.objects.get(user=request.user, status = True)
    except:
        messages.warning(request, "There are multiple address, only one should be activated.")

    return render(request, "core/checkout.html", {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'shipping_cost': shipping_cost,
            "delivery": delivery,
            "delivery_total_cost": delivery_total_cost,
            'order': order,
            'success_redirect_url': full_success_redirect_url,
            'failure_redirect_url': full_failure_redirect_url,
            'active_address':active_address,
        })


def razorpay_payment_status(request):
    # Get the response from Razorpay
    response = request.POST

    # Verify the payment signature
    razorpay_client = razorpay.Client(key_id="settings.RAZORPAY_KEY_ID", key_secret="settings.SECRET_KEY")
    razorpay_signature = response["razorpay_signature"]

    if razorpay_client.utility.verify_payment_signature(razorpay_signature, response):
        # The payment signature is valid

        # Get the payment ID from the response
        razorpay_payment_id = response["razorpay_payment_id"]

        # Check the payment status
        payment = razorpay_client.payment.fetch(razorpay_payment_id)

        if payment.status == "captured":
            # The payment is successful

            # Get the CartOrder object
            cart_order = CartOrder.objects.get(Q(razorpay_payment_id=razorpay_payment_id))

            # Update the paid_status field
            cart_order.paid_status = True

            # Save the CartOrder object
            cart_order.save()

            # Check the paid_status field
            if cart_order.paid_status:
                # The paid_status is true
                print("The paid_status is true")
            else:
                # The paid_status is false
                print("The paid_status is false")
            

            return JsonResponse({"status": "success"})
        else:
            # The payment is failed
            return JsonResponse({"status": "failed"})
    else:
        # The payment signature is invalid
        return JsonResponse({"status": "invalid_signature"})


@login_required    
def payment_completed_view(request):
    # product = Product.objects.get(pid=pid)
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount+=int(item['qty'])*float(item['price'])

        if cart_total_amount>=1000:
            shipping_cost=0
            delivery_total_cost = cart_total_amount
        else:
            shipping_cost=100
            delivery_total_cost = cart_total_amount+shipping_cost
        if cart_total_amount<500:
            delivery=0
        else:
            delivery=1
        return render(request, "core/payment-completed.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, 'shipping_cost':shipping_cost, "delivery":delivery, "delivery_total_cost":delivery_total_cost})


@login_required    
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')


@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)
    # try:
    #     orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count").annotate(user=request.user).values("user")
    #     month = []
    #     total_orders = []

    #     for o in orders:
    #         month.append(calendar.month_name[o["month"]])
    #         total_orders.append(o['count'])

    # except:
    #     orders=None
    #     month = ["September"]
    #     total_orders = ["0"]
    
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user = request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address Added Successfully.")
        return redirect("core:customer-dashboard")
    
    
    # return render(request, 'core/dashboard.html')
    context = {
        "orders_list":orders_list,
        "address":address,
        # "orders":orders,
        # "month":month,
        # "total_orders":total_orders,
    }
    return render(request, 'core/dashboard.html',context)

def order_detail(request,id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)
    context = {
        "products": products
    }

    return render(request, 'core/order-detail.html',context)


def vendor_dashboard(request):
    return render(request ,'core/vendor-dashboard.html')

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean":True})

@login_required
def wishlist_view(request):
    wishlist = wishlist_model.objects.all()
    context = {
        "wishlist":wishlist
    }

    return render(request, "core/wishlist.html", context)

def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    wishlist_count = wishlist_model.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)
    
    if wishlist_count > 0:
        context = {
            "bool":True,
        }

    else:
        new_wishlist = wishlist_model.objects.create(
            product=product,
            user=request.user
        )
        context ={
            "bool":True,    
        }

    return JsonResponse(context)


def delete_from_wishlist(request):
    pid = request.GET['id']
    wishlist = wishlist_model.objects.filter(user=request.user)

    product = wishlist_model.objects.get(id=pid)
    delete_product = product.delete()

    context = {
        "bool":True,
        "wishlist":wishlist,
    }

    wishlist_json = serializers.serialize('json', wishlist)
    data = render_to_string("core/async/wishlist-list.html", context)
    return JsonResponse({"data":data, "wishlist":wishlist_json})


def contact(request):
    return render(request, "core/contact.html")

def ajax_contact(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool":True,
        "message": "Message Sent Successfully"
    }

    return JsonResponse({"data":data})

def about_us(request):
    return render(request, "core/about-us.html")

def purchase_guide(request):
    return render(request, "core/purchase-guide.html")

def privacy_policy(request):
    return render(request, "core/privacy-policy.html")

def terms_of_service(request):
    return render(request, "core/terms-of-service.html")


def compare(request):
    return render(request, "core/compare.html")