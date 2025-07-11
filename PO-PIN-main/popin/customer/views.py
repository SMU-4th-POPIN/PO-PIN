from django.shortcuts import render
from adpage.models import Notice, NoticeImage

from django.http import JsonResponse
import json

# Create your views here.

def information(request):
    return render(request, 'information.html')

def notice(request):
    noticeList = Notice.objects.all().order_by('-is_pinned', '-created_at')
    notice_list = []
    
    for notice in noticeList:
        notice_list.append({
            'id' : notice.id,
            'title' : notice.title,
            'created_at' : notice.created_at.strftime('%Y-%m-%d'),
            'views': notice.views,
            'notice_type':notice.notice_type,
        })
    
    context = {
        "notice_list":notice_list,
    }
    return render(request, 'notice.html', context)

def filter_notice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notice_type = data.get('notice_type', '')

            notices = Notice.objects.all()
            if notice_type != "전체":
                notices = notices.filter(notice_type=notice_type)

            notice_list = [{
                'id': n.id,
                'title': n.title,
                'created_at': n.created_at.strftime('%Y-%m-%d'),
                'views': n.views,
                'notice_type': n.notice_type,
            } for n in notices.order_by('-is_pinned','-created_at')]

            return JsonResponse({'notices': notice_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)


def notice_view(request, id):
    notice = Notice.objects.get(id=id)
    notice.views += 1
    notice.save()
    
    notice_images = NoticeImage.objects.filter(notice=notice)
    print(notice_images)
    
    images = []
    
    for image in notice_images:
        images.append(image.image)

    context = {
        'id':notice.id,
        'notice_type':notice.notice_type,
        'title': notice.title,
        'content':notice.content,
        'images':images,
    }
    return render(request, 'notice_view.html', context)

def QnA(request):
    return render(request, 'Q&A.html')