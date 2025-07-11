from django.shortcuts import render


def main(request):
    return render(request, 'pocadeco/main.html')
def mydecolist(request):
    return render(request, 'pocadeco/mydecolist.html')
