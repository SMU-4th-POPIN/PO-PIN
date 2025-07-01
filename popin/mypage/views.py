from django.shortcuts import render

def showMybiasModal(request):
    return render(request,'mypage/showMybiasModal.html')

def pchange(request):
    return render(request,'mypage/pchange.html')

def mypage(request):
    return render(request,'mypage/myp
    age.html')
