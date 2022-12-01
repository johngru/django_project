from django.shortcuts import render
from app_one.forms import UserForm, UserProfileInfoForm



# Imports for Login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout



# Create your views here.
def index(request):
    return render(request,'app_one/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_info = UserProfileInfoForm(data=request.POST)

        #Check for valid forms
        if user_form.is_valid() and profile_info.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_info.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()


            registered = True

        else:
            print(user_form.errors, profile_info.errors)
    

    else:
        user_form = UserForm()
        profile_info = UserProfileInfoForm()


    return render(request, 'app_one/registration.html',context={'registered':registered,
    "UserForm":user_form, "UserProfileInfoForm":profile_info})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(username=username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")


        else:
            print("User tried logging in unsuccessfully")
            print(f"Username: {username}\nPassword: {password}")
            return HttpResponse("Invalid login details supplied!")

    else:
        return render(request, "app_one/login.html", {})

