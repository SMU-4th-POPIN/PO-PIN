from django.shortcuts import render


def login(request):
    return render(request,"accounts/login.html")
def signup(request):
    return render(request,"accounts/signup.html")
def FM(request):
    return render(request,"accounts/FM.html")


