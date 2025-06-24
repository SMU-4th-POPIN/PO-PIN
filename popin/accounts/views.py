from django.shortcuts import render ,redirect
from idols.models import Group, Member  
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('landing')  # 로그인 성공
        else:
            messages.error(request, '로그인 실패!')

    return render(request, 'accounts/login.html')  # ← 항상 반환!

def signup(request):
    if request.method == 'POST':
        # ... 회원가입 처리 로직 ...
        return redirect('accounts:login')  # 또는 render()
    return render(request, 'accounts/signup.html')  # ← 이게 꼭 있어야 함!

 



def FM(request):
    return render(request,"accounts/FM.html")


