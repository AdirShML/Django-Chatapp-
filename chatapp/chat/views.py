from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest


VALID_CHAT_ROOMS = ['room1', 'room2', 'room3']

# the main page or the 'lobby' ---- create user or login to excisting one to see content
@ login_required
def main_page(request):
    return render(request, 'chat/chatlobby.html', {'user': request.user})


# view of the available chat rooms
@ login_required
def room_view(request, room_name):
    if room_name not in VALID_CHAT_ROOMS:
         return HttpResponseBadRequest("Invalid room name")
    
    return render(request, 'chat/room.html', {"room_name": room_name})


# login an excisting user
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
             login(request, user)
             return redirect('main')
        
        else:
             messages.error(request, 'invalid input, please enter correct username or create one')
             return redirect('login')
        
        
    return render(request, 'chat/loginpage.html')    


# signing up page, to keep it simple, i choose to use built-in django User model
def signup_page(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        new_user = authenticate(username=username, password=password)
        if new_user is not None:
            login(request, new_user)
            messages.success(request, "Registration successful.")
            return redirect('main') 
    else:
        return render(request, 'chat/signup.html')
    

# logout user
def logout_user(request):
    logout(request)
    return redirect('login')  







