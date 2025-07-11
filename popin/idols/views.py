from django.http import JsonResponse
from django.db.models import Q
from idols.models import Group, Member

def idol_search_api(request):
    query = request.GET.get("q", "").strip()

    groups = Group.objects.filter(
        Q(name__icontains=query) | Q(name_en__icontains=query)
    ).values("id", "name", "name_en","gender")

    members = Member.objects.filter(
        Q(name__icontains=query) |
        Q(name_en__icontains=query) |
        Q(group__name__icontains=query) |
        Q(group__name_en__icontains=query)
    ).values("id", "name", "name_en", "group__name", "group__gender")  # gender 같이 보내기

    return JsonResponse({
        "groups": list(groups),
        "members": list(members)
    })