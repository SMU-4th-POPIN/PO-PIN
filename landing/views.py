from django.shortcuts import render
from photocard.models import Photocard

from django.db.models import Count

def landing(request):
    photocards = Photocard.objects.select_related('member__group').annotate(
        wish_count=Count('wished_by_users')).order_by('-wish_count')[:4]
    context = {"photocards":photocards}
    return render(request, 'landing.html', context)