from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib import messages

# about us 

def login(request):
    if request.method == "GET" :
        return render(request,'core/pages/login.html', {messages:messages})
    print(request.method)
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login_user(request,user)
        return redirect('home')
    else:
        messages.error(request,"Username and password doesn't match")
        return render(request,'core/pages/login.html')

def logout(request):
    logout_user(request)
    return redirect('home')
# custom 404 view
def custom_404(request, exception):
    raise Exception("Sorry, no numbers below zero")
    return render(request, 'core/404.html', status=404)

def handler404(request, *args, **argv):
    return render(request,"core/404.html",status=404)

def handler500(request, *args, **argv):
    return render(request,"core/500.html",status=500)