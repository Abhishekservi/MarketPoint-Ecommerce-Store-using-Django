from django.urls import path, include
from core.views import *

app_name="core"

urlpatterns =[

    #HomePage
    path("",index,name="index"),
    path("products/",product_list_view,name = "product-list"),
    path("product/<pid>",product_detail_view,name = "product-detail"),

    #Category
    path("category/",category_list_view,name = "category-list"),
    path("category/<cid>/",category_product_list_view, name = "category-product-list"),

    #Vendor
    path("vendors/",vendor_list_view,name = "vendor-list"),
    path("vendor/<vid>",vendor_detail_view,name = "vendor-detail"),

    #Tags
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),

    #Reviews
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"),

    #Search
    path("search/", search_view, name="search"),

    #Filter product url
    path("filter-products/", filter_product, name="filter-product"),

    #Add to cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    #Cart Page Url
    path("cart/", cart_view, name="cart"),

    #Delete Item from Cart
    path("delete-from-cart/", delete_item, name="delete-from-cart"),

    #Update the cart
    path("update-cart/", update_cart, name="update-cart"),

    #Delete full cart
    path("clear-cart/", clear_cart, name="clear-cart"),

    #CheckOut Page
    path("checkout/", checkout_view, name="checkout"),

    # #Paypal Url
    # path("paypal/", include('paypal.standard.ipn.urls')),

    #Payment Succesfull
    path("checkout/payment-completed/", payment_completed_view, name="payment-completed"),

    #Payment Failed
    path("checkout/payment-failed/", payment_failed_view, name="payment-failed"),

    #Customer Dashboard
    path("dashboard/", customer_dashboard, name="customer-dashboard"),

    #Order Detail URL
    path("dashboard/order/<int:id>/", order_detail, name="order-detail"),

    #Vendor Dashboard
    path("vendor-dashboard/", vendor_dashboard, name="vendor-dashboard"),

    #Making Address Default
    path("make-default-address/", make_address_default, name="make-default-address"),

    #Wishlist Page
    path("wishlist/", wishlist_view, name="wishlist"),

    #Adding to wishlist
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),

    #Delete from wishlist
    path("delete-from-wishlist/", delete_from_wishlist, name="delete-from-wishlist"),

    #COntact Page
    path("contact-us/", contact, name="contact"),

    #About us
    path("about-us/", about_us, name="about-us"),

    #Purchase Guide
    path("purchase-guide/", purchase_guide, name="purchase-guide"),

    #Privacy Policy
    path("privacy-policy/", privacy_policy, name="privacy-policy"),

    #Terms of service
    path("terms/", terms_of_service, name="terms"),

    #Compare
    path("compare/", compare, name="compare"), 

]