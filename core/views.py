from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count

from core.models import Product, Category, Vendor, CartOrderItems, CartOrder, ProductImages, ProductReview, wishlist, Address



# Create your views here.
def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status="published", featured=True).order_by("-id")

    context={
        "products":products
    }
    return render(request, "core/index.html",context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published").order_by("-id")

    context={
        "products":products
    }
    return render(request, "core/product-list.html",context)


def category_list_view(request):

    categories = Category.objects.all()
    # categories = Category.objects.all().annotate(product_count=Count("products"))
    
    context ={
        "categories":categories
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

    p_image = product.p_images.all()

    context ={
        "P":product,
        "p_image":p_image
    }
    return render(request, "core/product-detail.html", context)