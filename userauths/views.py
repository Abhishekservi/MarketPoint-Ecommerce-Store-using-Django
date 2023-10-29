from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User


def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey! You are already logged in.")
        return redirect("core:index")

    if request.method =="POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Hey {username}, Your account was created successfully.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password = form.cleaned_data['password1']
                                    )
            login(request, new_user)
            return redirect("core:index")

    else:   
        form = UserRegisterForm()


    context ={
        'form':form
    }

    return render(request, "userauths/sign-up.html",context)


# def login_view(request):
#     if request.user.is_authenticated:
#         messages.warning(request, f"Hey! You are already LoggedIn.")
#         return redirect("core:index")
    
#     if request.method == "POST":
#         email = request.POST.get("email") # This is the email user passes in login page
#         password = request.POST.get("password") # This is the passwird from login

#         try:
#             user = User.objects.get(email=email) # Now the database checks for if the email is already present in the database
#             if user is not None:
#                 login(request, user)
#                 messages.success(request,"You are logged in succussfully")
#                 return redirect("core:index")
#             else:
#                 messages.warning(request, "User Does Not Exist. Create an Account.")
    
        
#         except:
#             messages.warning(request,f"User with {email} does not exist")

#         #This command below checks if users email is equal to the data bases emnail and same for the password
#         user = authenticate(request,email=email,password=password)        

        
#     context={
        
#     }
    
#     return render(request, "userauths/sign-in.html",context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey! You are already logged in.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")  # This is the email user passes on the login page
        password = request.POST.get("password")  # This is the password from the login form

        try:
            user = User.objects.get(email=email)  # Check if the email is in the database

            # If the email exists, then attempt to authenticate the user
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in successfully")
                return redirect("core:index")
            else:
                messages.warning(request, "Invalid email or password")
        except User.DoesNotExist:
            messages.warning(request, f"User with email {email} does not exist")

    context = {}
    return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.success(request,"You are Logged out.")
    return redirect("userauths:sign-in")