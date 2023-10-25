console.log("barobar hai sab");

const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

$("#commentForm").submit(function(e){
    e.preventDefault();

    let date = new Date();
    let time = date.getDay() + " " + monthNames[date.getMonth] + ", " + date.getFullYear();


    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(res){
            console.log("Comment Save to Db.....");

            if(res.bool == true){
                $("#review-res").html("Review added successfully.")
                $(".hide-comment-form").hide()
                $(".add-review").hide()
                
                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html+='<div class="user justify-content-between d-flex">'
                    _html+='<div class="thumb text-center">'
                    _html+='<img src="https://nwsid.net/wp-content/uploads/2015/05/dummy-profile-pic.png" alt="" />'
                    _html+='<a href="#" class="font-heading text-brand">'+ res.context.user +'</a>'
                    _html+='</div>'

                    _html+='<div class="desc">'
                    _html+='<div class="d-flex justify-content-between mb-10">'
                    _html+='<div class="d-flex align-items-center">'
                    _html+='<span class="font-xs text-muted">' + time + '</span>'
                    _html+='</div>'

                    for(var i = 1; i<=res.context.rating; i++){
                        _html += '<i class="fa-solid fa-star" style="color: #f6d813;"></i>'
                    }

                    _html+='</div>'
                    _html+='<p class="mb-10">'+ res.context.review +'</p>'
                    
                    _html+='</div>'
                    _html+= '</div>'
                    _html+='</div>'
                    $(".comment-list").prepend(_html)

            }   
 
        }
    })
})



$(document).ready(function (){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("Check box is clicked");

        let filter_object = {}


        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price
        filter_object.max_price = max_price

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")


            console.log("Filter value is:", filter_value);
            console.log("Filter key is:", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })
        
        })
        console.log("Filter object is: ", filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Trying to filter product....");
            },
            success:function(response){
                console.log(response);
                console.log("Data filtered successfully...");
                $('#filtered-product').html(response.data)
            }
        })
    })

    $("#max_price").on("blur",function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        // console.log("Current Price is:", current_price);
        // console.log("Min Price is:", min_price);
        // console.log("Max Price is:", max_price);

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            // console.log("Price Error.")

            min_price= Math.round(min_price*100)/100
            max_price= Math.round(max_price*100)/100

        
            // console.log("Max Price is:", max_price);
            // console.log("Min Price is:", min_price)

            alert("Price must be between ₹" + min_price + " and ₹" + max_price);
            $(this).val(min_price)
            $(this).focus()
            $('#range').val

        }
    })

    //ADD to cart functionality
    $(".add-to-cart-btn").on("click", function(){
        
        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()
        
        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text()
        
        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()

        console.log("Quantity:", quantity);
        console.log("title:",  product_title);
        console.log("price:",  product_price);
        console.log("id:",  product_id);
        console.log("PID:", product_pid);
        console.log("Image:", product_image);
        console.log("index:", index);
        console.log("Current Element:", this_val);


        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding product to Cart...");
            },
            success: function(response){
                this_val.html("✔️");
                console.log("Added Product to cart!");
                $(".cart-items-count").text(response.totalcartitems)
            }, 
        })

    })


    $(document).on("click", ".delete-product", function() {
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
    
        console.log("Product Id:", product_id);
    
        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function() {
                this_val.hide();
            },
            success: function(response) {
                this_val.show();
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data);
            }
        });
    });


    $(document).on("click", ".decrement-btn", function() {
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        let product_quantity = $(".product-qty-" + product_id).val()
        let productPrice = $(".current-product-price-" + product_id).text()
        let newPrice = product_quantity * productPrice;
        
        
        console.log("Product Id:", product_id);
        console.log("Product qty:", product_quantity);
        console.log("ProductPrice:", productPrice );
        console.log("newPrice:", newPrice);
            
        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty":product_quantity,
                "price":productPrice,
                "newPrice":newPrice
            },
            dataType: "json",
            // beforeSend: function() {
            //     this_val.hide();
            // },
            success: function(response) {
                // this_val.show();
                $(".cart-items-count").text(response.totalcartitems);
                $('.newPrice[data-item-id="'+product_id+'"]').text(newPrice); 
                $("#cart-list").html(response.data);

            }
        });
    });


    $(document).on("click", ".increment-btn", function() {
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        let product_quantity = $(".product-qty-" + product_id).val()
        let productPrice = $(".current-product-price-" + product_id).text()
        let newPrice = product_quantity * productPrice;


        console.log("Product Id:", product_id);
        console.log("Product qty:", product_quantity);
        console.log("ProductPrice:", productPrice );
        console.log("newPrice:", newPrice);

        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty":product_quantity,
                "price":productPrice,
                "newPrice":newPrice
            },
            dataType: "json",
            
            success: function(response) {
                
                $(".cart-items-count").text(response.totalcartitems);
                $('.newPrice[data-item-id="'+product_id+'"]').text(newPrice);
                $("#cart-list").html(response.data);
            }
        });
    });
    
    // Clear cart button click
    $(document).on("click", "#clear-cart", function() {

        // AJAX request to clear cart
        $.ajax({
        url: '/clear-cart',
        success: function() {
        
            // Reload page to clear cart 
            location.reload();
        
        }
        });
    
    })


    //Making Default Adddress
    $(document).on("click",".make-default-address", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)


        console.log("ID is:", id);
        console.log("Element is:", this_val);

        $.ajax({
            url: "/make-default-address",
            data: {
                "id":id
            },
            dataType: 'json',
            success:function(response){
                console.log("Address Made Default.");
                if (response.boolean == true){

                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check"+id).show()
                    $(".button"+id).hide()

                }
            }
        })

    })


    //Adding to wishlist

    $(document).on("click", ".add-to-wishlist",function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("Product Id is:", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Adding to wishlist...");
            },
            success: function(response){
                this_val.html("✔️")
                if (response.bool === true){
                    console.log("Added to wishlist .....");
                }
            }
        })
    })

    // Remove from wishlist
    $(document).on("click", ".delete-wishlist-product", function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("Wishlist id is:", wishlist_id);

        $.ajax({
            url:"/delete-from-wishlist",
            data: {
                "id": wishlist_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Deleting product from wishlist...");
            },
            success: function(response){
                $("#wishlist-list").html(response.data)
            }
        })
    })
    
})




// //ADD to cart functionality
// $("#add-to-cart-btn").on("click", function(){
//     let quantity = $("#product-quantity").val()
//     let product_title = $("#product-title").val()
//     let product_id = $("#product-id").val()
//     let product_price = $("#current-product-price").text()
//     let this_val = $(this)

//     console.log("Quantity", quantity);
//     console.log("title",  product_title);
//     console.log("price",  product_price);
//     console.log("id",  product_id);
//     console.log("Current Element:", this_val);


//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             'id': product_id,
//             'qty': quantity,
//             'title': product_title,
//             'price': product_price,
//         },
//         dataType: 'json',
//         beforeSend: function(){
//             console.log("Adding product to Cart...");
//         },
//         success: function(response){
//             this_val.html("Item added to cart");
//             console.log("Added Product to cart!");
//             $(".cart-items-count").text(response.totalcartitems)
//         }, 
//     })

// })


//Making 