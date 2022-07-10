from django.shortcuts import render, redirect, get_object_or_404
from  django.contrib.auth import authenticate, login, logout, get_user_model
from  django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from core import views 

User = get_user_model()


@login_required(login_url='login/')
def home(request):
    return redirect(views.home)
    

def register(request):
    """ Handles user registration flow

    POST request - register a new user.
    """
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        password2 = form.cleaned_data["password2"]
        try:
           user = User.objects.create_user(username,email,password)
           if user != None:
               login(request,user)
               return redirect(views.auth_spotify)
        except User.DoesNotExist:
            user = None
            messages.error(request,"Please check the data you entered")
            request.session["register_error"] = 1
        
    context={"form":form}
    return render(request,"register.html",context)

def login_user(request):
    """Handles user login flow 
    Authenticates username and password. verify credentials are met.
    """
    
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        
        #if user exists in sessions db redirect to homepage.
        if user != None:
            login(request,user)
            return redirect(views.home)
        else:
            request.session["invalid_user"] = 1
        
    context={"form":form}
    return render(request,"login.html",context)

def logout_user(request):
    """ Handles user logout flow 
    Removes the authenticated user's ID from the request and deletes their session data.
    """
    logout(request)
    # request.user == Anonymous user
    return redirect("/login")