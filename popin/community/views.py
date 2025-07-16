from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import SharingPost, SharingTag, SharingImage
from django.db.models import Avg
from datetime import datetime, timedelta
from django.core.files.storage import default_storage
from django.db import transaction
from django.http import HttpResponse
from community.models import ExchangeReview, ReviewImage, ReviewTag
from signupFT.models import User  # 너의 커스텀 유저 모델 import
from django.contrib import messages
from .models import CompanionPost, CompanionTag, CompanionImage
from django.views.decorators.csrf import csrf_exempt
from community.models import ProxyPost, ProxyImage, ProxyTag
from django.utils.timezone import make_aware
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from community.models import StatusPost, StatusImage, StatusTag
from itertools import chain
from operator import attrgetter
from django.db.models import Q
from django.core.paginator import Paginator
from .models import ProxyStatus
from community.models import SharingStatus  
from community.models import CompanionPost, CompanionComment
from django.utils import timezone
from community.models import  StatusStatus 
from django.shortcuts import render
from django.db.models import Count, Avg
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404
from signupFT.models import User
from community.models import (
    CompanionPost, SharingPost, ProxyPost, StatusPost, ExchangeReview
)
from community.models import (
    BlockedCompanionPost, BlockedSharingPost,
    BlockedProxyPost, BlockedStatusPost, BlockedExchangeReview
)
from community.models import (
    CompanionPost,
    SharingPost,
    ProxyPost,
    StatusPost,
    ExchangeReview,  
)
User = get_user_model()
#########  urls.py 순서대로 정리함 

def updateC(request) :
    return render(request,'update/chgR_update.html')

def updateCo(request) :
    return render(request,'update/comp_update.html')

def updateP(request) :
    return render(request,'update/proxy_update.html')

def updateSh(request) :
    return render(request,'update/shar_update.html')

def updateS(request) :
    return render(request,'update/status_update.html')


def proxyview(request) :
    return render(request,'chgReview/proxy_view.html')

def companionview(request) :
    return render(request,'chgReview/comp_view.html')

def sharingview(request) :
    return render(request,'chgReview/shar_view.html')

def statusview(request) :
    return render(request,'chgReview/status_view.html')




def chgReviewmain(request):
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    weekly_reviews = ExchangeReview.objects.filter(created_at__gte=start_of_week)
    weekly_count = weekly_reviews.count()
    average_score = ExchangeReview.objects.aggregate(avg_score=Avg("overall_score"))["avg_score"]
    average_score = round(average_score or 0, 1)

    query = request.GET.get('q', '')
    if query:
        filtered_reviews = ExchangeReview.objects.filter(
            Q(title__icontains=query) | Q(writer__user_id__icontains=query)
        ).order_by('-created_at')
    else:
        filtered_reviews = ExchangeReview.objects.all().order_by('-created_at')

    paginator = Paginator(filtered_reviews, 7)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "weekly_count": weekly_count,
        "average_score": average_score,
        "page_obj": page_obj,
        "query": query,
    }

    return render(request, "chgReview/main.html", context)


################################################################################
##교환/판매 상세보기 

def chgReviewview(request, pk):
    post = get_object_or_404(
        ExchangeReview.objects.prefetch_related('tags', 'images'),
        id=pk
    )

    # 조회수 증가 (선택)
    post.views += 1
    post.save(update_fields=["views"])

    return render(request, 'chgReview/chgR_view.html', {
        'post': post
    })
################################################################################

# 교환후기글 수정 
def chgReview_update(request, pk):
    post = get_object_or_404(ExchangeReview, id=pk)

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.overall_score = request.POST.get("overall_score")
        post.save()
        return redirect('chgReview:chgReviewview', pk=post.id)

    return render(request, 'chgReview/chgR_edit.html', {'post': post})


   
################################################################################
## 최근게시글
def recent(request):
    
    return render(request, 'community/community_recent.html')

#############################################################################
# 동행모집글 작성

def write_companion(request):
    if request.method == "POST":

        try:
            # 1. 사용자
            user_id = request.session.get('user_id')
            user = User.objects.get(user_id=user_id)

            # 2. 기본 정보
            title = request.POST.get('title')
            artist = request.POST.get('artist')
            category = request.POST.get('category')
            location = request.POST.get('location')
            content = request.POST.get('content')
            max_people = request.POST.get('max_people')  
            tags = request.POST.get('tags', '')

            # 3. 날짜 + 시간 → datetime 필드
            date_str = request.POST.get('eventDate')
            time_str = request.POST.get('eventTime')
            event_datetime = timezone.make_aware(datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M"))

            # 4. 게시글 저장
            post = CompanionPost.objects.create(
                title=title,
                artist=artist,
                category=category,
                location=location,
                content=content,
                max_people=max_people,
                event_date=event_datetime,
                author=user,
            )


            # 5. 태그 처리
            tag_list = [tag.strip().lstrip('#') for tag in tags.split(',') if tag.strip()]
            for tag_name in tag_list:
                tag_obj, _ = CompanionTag.objects.get_or_create(name=tag_name)
                post.tags.add(tag_obj)


            # 6. 이미지 저장
            for file in request.FILES.getlist('images'):
                CompanionImage.objects.create(post=post, image=file)


            return redirect('community:companion')
        except Exception as e:
            import traceback
            print(traceback.format_exc())  # 콘솔 확인용
            return render(request, 'community/community_write_companion.html', {'error': str(e)})
    
    return render(request, 'community/community_write_companion.html')
  ########################################################################################## 
    
## 대리구매글 작성

def write_proxy(request):

    if request.method == "POST":
        title = request.POST.get("title")
        artist = request.POST.get("artist")
        category = request.POST.get("category", "기타")
        status = request.POST.get("status", "모집중")


        # 날짜와 시간 조합 → DateTimeField에 맞게
        event_date = request.POST.get("eventDate")
        event_time = request.POST.get("eventTime")
        event_datetime = timezone.make_aware(datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M"))


        location = request.POST.get("location")
        max_people = request.POST.get('max_people')
        reward = request.POST.get("fee")
        description = request.POST.get("content")
        tag_string = request.POST.get("tags", "")

        # 세션에서 사용자 가져오기
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")  # 로그인 안 되어 있으면 로그인 페이지로


        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return render(request, "community/write_proxy.html", {"error": "사용자를 찾을 수 없습니다."})

        # 저장
        proxy_post = ProxyPost.objects.create(
            title=title,
            artist=artist,
            category=category,
            status=status,
            event_date=event_datetime,
            location=location,
            max_people=max_people,
            reward=reward,
            description=description,
            author=user
        )

        # 태그 처리
        tags = [t.strip().replace("#", "") for t in tag_string.split() if t.strip()]
        for tag_name in tags:
            tag_obj, _ = ProxyTag.objects.get_or_create(name=tag_name)
            proxy_post.tags.add(tag_obj)

        # 이미지 업로드
        images = request.FILES.getlist("images")
        for img in images:
            ProxyImage.objects.create(post=proxy_post, image=img)

        return redirect("community:main")  # 작성 완료 후 메인으로 이동

    
    return render(request, 'community/community_write_proxy.html')

#############################################
## 교환후기 글작성 
def write_review(request):
    if request.method == 'POST':
        try:
            # 세션에서 user_id 가져오기
            user_id = request.session.get('user_id')
            if not user_id:
                messages.error(request, "[오류] 로그인 정보가 없습니다.")
                return redirect('community:write_review')

            try:
                writer = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                messages.error(request, "[오류] 유저 정보를 찾을 수 없습니다.")
                return redirect('community:write_review')

            title = request.POST.get('title')
            content = request.POST.get('content')
            artist = request.POST.get('artist', '기타')
            method = request.POST.get('method')
            transaction_type = request.POST.get('transaction_type', '교환')
            score = int(request.POST.get('overall_score', 3))
            tag_str = request.POST.get('tags', '')
            partner_id = request.POST.get('partner')

            try:
                partner = User.objects.get(user_id=partner_id)
            except User.DoesNotExist:
                partner = writer  # fallback

            with transaction.atomic():
                review = ExchangeReview.objects.create(
                    writer=writer,
                    partner=partner,
                    title=title,
                    content=content,
                    artist=artist,
                    method=method,
                    transaction_type=transaction_type,
                    overall_score=score
                )

                if tag_str:
                    tag_list = [tag.lstrip('#') for tag in tag_str.strip().split()]
                    for tag in tag_list:
                        tag_obj, _ = ReviewTag.objects.get_or_create(name=tag)
                        review.tags.add(tag_obj)

                for img in request.FILES.getlist('images'):
                    ReviewImage.objects.create(review=review, image=img)

            messages.success(request, "리뷰가 저장되었습니다.")
            return redirect('community:main')

        except Exception as e:
            print("[리뷰 저장 실패]", e)
            messages.error(request, f"[오류] {str(e)}")
            return redirect('community:write_review')

    return render(request, 'community/community_write_review.html')
#########################################

#나눔 
def write_sharing(request):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                messages.error(request, "[오류] 로그인 정보가 없습니다.")
                return redirect('community:write_sharing')

            try:
                author = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                messages.error(request, "[오류] 작성자 정보를 찾을 수 없습니다.")
                return redirect('community:write_sharing')

            # POST 데이터 받기
            title = request.POST.get('title')
            content = request.POST.get('content')
            artist = request.POST.get('artist', '기타')
            category = request.POST.get('category')
            sharing_type = request.POST.get('type')
            if not sharing_type: sharing_type = '오프라인'
            location = request.POST.get('location')
            requirement = request.POST.get('requirement')
            tag_str = request.POST.get('tags', '')
            share_date_str = request.POST.get('share_date')

            # 타입 누락 시 오류 처리
            if not sharing_type:
                messages.error(request, "[오류] 나눔 형태(type)는 필수 선택 항목입니다.")
                return redirect('community:write_sharing')

            # 날짜 변환
            share_date = None
            if share_date_str:
                naive_datetime = datetime.strptime(share_date_str, "%Y-%m-%dT%H:%M")
                share_date = make_aware(naive_datetime)

            with transaction.atomic():
                post = SharingPost.objects.create(
                    author=author,
                    title=title,
                    content=content,
                    artist=artist,
                    category=category,
                    type=sharing_type,  #  정확히 전달
                    share_date=share_date,
                    location=location,
                    requirement=requirement
                )

                # 태그 저장
                if tag_str:
                    tag_list = [tag.strip().lstrip('#') for tag in tag_str.split(',')]
                    for tag in tag_list:
                        tag_obj, _ = SharingTag.objects.get_or_create(name=tag)
                        post.tags.add(tag_obj)

                # 이미지 저장
                for img in request.FILES.getlist('images'):
                    SharingImage.objects.create(post=post, image=img)

            messages.success(request, "나눔 글이 저장되었습니다.")
            return redirect('community:main')

        except Exception as e:
            print("[나눔 저장 실패]", e)
            messages.error(request, f"[오류] {str(e)}")
            return redirect('community:write_sharing')

    return render(request, 'community/community_write_sharing.html')
#################################################################

 
@csrf_exempt
def write_status(request):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({'error': '로그인이 필요합니다.'}, status=403)

            user = User.objects.get(user_id=user_id)

            title = request.POST.get('title', '').strip()
            artist = request.POST.get('artist', '').strip()
            category = request.POST.get('category', '').strip()
            event_datetime_str = request.POST.get('event_datetime')
            event_datetime = parse_datetime(event_datetime_str) if event_datetime_str else None
            location = request.POST.get('location', '').strip()
            region = request.POST.get('region', '').strip()
            content = request.POST.get('content', '').strip()
            tag_string = request.POST.get('tags', '')
            tag_names = [tag.strip() for tag in tag_string.split(',') if tag.strip()]

            # 필수값 누락 시 예외
            if not (title and artist and category and event_datetime and location and content):
                return JsonResponse({'error': '필수 항목이 누락되었습니다.'}, status=400)

            # 게시글 저장
            post = StatusPost.objects.create(
                author=user,
                title=title,
                artist=artist,
                category=category,
                event_datetime=event_datetime,
                place=location,
                region=region,
                content=content
            )

            # 태그 저장
            for tag_name in tag_names:
                tag, _ = StatusTag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

            # 이미지 저장
            for image in request.FILES.getlist('images'):
                StatusImage.objects.create(post=post, image=image)

            return JsonResponse({'success': True})


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # GET 요청일 경우 템플릿 렌더링
    return render(request, 'community/community_write_status.html')
 #현황공유 작성



#######################################################################
# 메인페이지
def main(request):
    today = timezone.now().date()

    # 교환후기
    total_reviews = ExchangeReview.objects.count()
    avg_rating = ExchangeReview.objects.aggregate(avg=Avg('overall_score'))['avg'] or 0
    today_reviews = ExchangeReview.objects.filter(created_at__date=today).count()

    # 나눔 (SharingPost)
    sharing_active = SharingPost.objects.filter(status='진행중').count()
    sharing_completed = SharingPost.objects.filter(status='마감').count()
    sharing_today = SharingPost.objects.filter(created_at__date=today).count()

    # 대리구매 (ProxyPost)
    proxy_active = ProxyPost.objects.filter(status='모집중').count() + ProxyPost.objects.filter(status='긴급모집').count()
    proxy_completed = ProxyPost.objects.filter(status='마감').count()
    proxy_today = ProxyPost.objects.filter(created_at__date=today).count()

    # 현황공유 (StatusPost)
    status_active = StatusPost.objects.filter(status='진행중').count()
    status_total = StatusPost.objects.count()
    status_today = StatusPost.objects.filter(created_at__date=today).count()

    # 동행 (CompanionPost)
    companion_active = CompanionPost.objects.filter(status='모집중').count() + CompanionPost.objects.filter(status='진행중').count()
    companion_completed = CompanionPost.objects.filter(status='모집완료').count()
    companion_today = CompanionPost.objects.filter(created_at__date=today).count()

    # 최근 활동
    recent_items = []
    last_review = ExchangeReview.objects.order_by('-created_at').first()
    if last_review:
        recent_items.append({
            'title': f"{last_review.writer.nickname}님과의 교환 후기 등록",
            'meta': f"교환후기 · 별점 {last_review.overall_score}",
            'icon': '⭐',
            'time': last_review.created_at,
        })

    last_sharing = SharingPost.objects.order_by('-created_at').first()
    if last_sharing:
        recent_items.append({
            'title': last_sharing.title,
            'meta': f"오프라인 나눔 · 진행상태: {last_sharing.status}",
            'icon': '🎁',
            'time': last_sharing.created_at,
        })

    last_proxy = ProxyPost.objects.order_by('-created_at').first()
    if last_proxy:
        recent_items.append({
            'title': last_proxy.title,
            'meta': f"대리구매 · 상태: {last_proxy.status}",
            'icon': '🛒',
            'time': last_proxy.created_at,
        })

    last_status = StatusPost.objects.order_by('-created_at').first()
    if last_status:
        recent_items.append({
            'title': last_status.title,
            'meta': f"현황공유 · 상태: {last_status.status}",
            'icon': '📊',
            'time': last_status.created_at,
        })

    last_companion = CompanionPost.objects.order_by('-created_at').first()
    if last_companion:
        recent_items.append({
            'title': last_companion.title,
            'meta': f"동행모집 · 상태: {last_companion.status}",
            'icon': '👥',
            'time': last_companion.created_at,
        })

    recent_items = sorted(recent_items, key=lambda x: x['time'], reverse=True)[:5]

    context = {
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 1),
        'today_reviews': today_reviews,

        'sharing_active': sharing_active,
        'sharing_completed': sharing_completed,
        'sharing_today': sharing_today,

        'proxy_active': proxy_active,
        'proxy_completed': proxy_completed,
        'proxy_today': proxy_today,

        'status_active': status_active,
        'status_total': status_total,
        'status_today': status_today,

        'companion_active': companion_active,
        'companion_completed': companion_completed,
        'companion_today': companion_today,

        'recent_items': recent_items,
    }
    return render(request, 'community/main.html', context)
#########################################

def companion(request):
    query = request.GET.get('q', '')  # 검색어 받아오기

    if query:
        all_posts = CompanionPost.objects.filter(
            Q(title__icontains=query)
        ).order_by('-created_at')
    else:
        all_posts = CompanionPost.objects.all().order_by('-created_at')

    # 통계 수치
    ongoing_count = CompanionPost.objects.count()
    completed_count = CompanionPost.objects.filter(status='모집완료').count() 
    weekly_count = CompanionPost.objects.filter(created_at__week=timezone.now().isocalendar()[1]).count()

    # 페이지네이터
    paginator = Paginator(all_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'query': query,
        'ongoing_count': ongoing_count,
        'completed_count': completed_count,
        'weekly_count': weekly_count,
    }

    return render(request, 'companion/main.html', context)
###########################################################################
##### 대리구매 게시판

def proxy(request):
    # 🔍 검색어 받기
    query = request.GET.get('q', '')  # 일반 검색어

    # 🔎 기본 queryset
    all_posts = ProxyPost.objects.all()

    if query:
        all_posts = all_posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    all_posts = all_posts.order_by('-created_at')

    # 📊 통계 계산
    ongoing_count = ProxyPost.objects.count()  # 조건 추가 가능
    completed_count = ProxyPost.objects.filter(status=ProxyStatus.DEADLINE).count()
    weekly_count = ProxyPost.objects.filter(
        created_at__week=timezone.now().isocalendar()[1]
    ).count()

    # 📄 페이지네이션
    paginator = Paginator(all_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 💬 템플릿 전달
    context = {
        'posts': page_obj,
        'ongoing_count': ongoing_count,
        'completed_count': completed_count,
        'weekly_count': weekly_count,
        'query': query,  # 🔁 HTML에서 검색어 유지용
    }

    return render(request, 'proxy/main.html', context)
#############################################################################################
##### 나눔 게시판

def sharing(request):
    # 1. 검색어 가져오기
    query = request.GET.get('q', '')

    # 2. 필터링 (제목 기준)
    if query:
        all_posts = SharingPost.objects.filter(title__icontains=query).order_by('-created_at')
    else:
        all_posts = SharingPost.objects.all().order_by('-created_at')

    # 3. 통계 수치 계산
    ongoing_count = SharingPost.objects.count()
    completed_count = SharingPost.objects.filter(status=SharingStatus.CLOSED).count()
    weekly_count = SharingPost.objects.filter(created_at__week=timezone.now().isocalendar()[1]).count()

    # 4. 페이지네이션
    paginator = Paginator(all_posts, 6)  # 페이지당 6개
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'ongoing_count': ongoing_count,
        'completed_count': completed_count,
        'weekly_count': weekly_count,
        'query': query,  # 템플릿에서 검색어 유지하려면 필요
    }
    return render(request, 'sharing/main.html', context)
 #####################################################   

##### 현황공유 게시판

def status(request):
    query = request.GET.get('q', '')

    if query:
        all_posts = StatusPost.objects.filter(
            Q(title__icontains=query)
        ).order_by('-created_at')
    else:
        all_posts = StatusPost.objects.all().order_by('-created_at')

    # 통계 수치 계산
    ongoing_count = StatusPost.objects.count()
    completed_count = StatusPost.objects.filter(status=StatusStatus.CLOSED).count()
    weekly_count = StatusPost.objects.filter(
        created_at__week=timezone.now().isocalendar()[1]
    ).count()

    # 페이지네이션
    paginator = Paginator(all_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'ongoing_count': ongoing_count,
        'completed_count': completed_count,
        'weekly_count': weekly_count,
        'query': query  # 검색어 유지
    }
    return render(request, 'status/main.html', context)


##################


def companionview(request, pk):
    post = get_object_or_404(CompanionPost, pk=pk)
    post.views += 1
    post.save(update_fields=["views"])

    return render(request, 'chgReview/comp_view.html', {
        'post': post,
        'title': post.title,
        'artist': post.artist,
        'category': post.category,
        'location': post.location,
        'content': post.content,
        'tags': post.tags.all(),
        'event_date': post.event_date,
        'max_people': post.max_people,
        'participants': post.participants.all(),
        'status': post.status,
        'images': post.images.all(),
    })


def sharingview(request, pk):
    post = get_object_or_404(SharingPost, pk=pk)
    post.views += 1
    post.save(update_fields=["views"])

    return render(request, 'chgReview/shar_view.html', {
        'post': post,
        'title': post.title,
        'content': post.content,
        'artist': post.artist,
        'requirement': post.requirement,
        'category': post.category,
        'type': post.type,
        'share_date': post.share_date,
        'location': post.location,
        'tags': post.tags.all(),
        'status': post.status,
        'images': post.images.all(),
    })


def proxyview(request, pk):
    post = get_object_or_404(ProxyPost, pk=pk)
    post.views += 1
    post.save(update_fields=["views"])

    return render(request, 'chgReview/proxy_view.html', {
        'post': post,
        'title': post.title,
        'artist': post.artist,
        'category': post.category,
        'status': post.status,
        'event_date': post.event_date,
        'location': post.location,
        'max_people': post.max_people,
        'reward': post.reward,
        'description': post.description,
        'tags': post.tags.all(),
        'participants': post.participants.all(),
        'images': post.images.all(),
    })
    
    
def statusview(request, pk):
    post = get_object_or_404(StatusPost, pk=pk)
    post.views += 1
    post.save(update_fields=["views"])
        
    return render(request, 'chgReview/status_view.html', {
        'post': post,
        'title': post.title,
        'artist': post.artist,
        'category': post.category,
        'status': post.status,
        'event_datetime': post.event_datetime, 
        'place': post.place,                    
        'region': post.region,                  
        'content': post.content,
        'tags': post.tags.all(),
        'images': post.images.all(),
    })


# 수정 
from django.utils.timezone import make_aware
from datetime import datetime

def updateCo(request, pk):
    post = get_object_or_404(CompanionPost, pk=pk)

    if request.method == "POST":
        print("🔧 [updateCo POST DATA]", request.POST)

        post.title = request.POST.get('title', post.title)
        post.artist = request.POST.get('artist', post.artist)
        post.category = request.POST.get('category', post.category)
        post.location = request.POST.get('location', post.location)
        post.content = request.POST.get('content', post.content)
        post.max_people = request.POST.get('max_people', post.max_people)
        post.region = request.POST.get('region', post.region)
        
        # 태그
        tag_string = request.POST.get('tags', '')
        post.tags.clear()
        for tag_name in [t.strip().lstrip('#') for t in tag_string.split(',') if t.strip()]:
            tag_obj, _ = CompanionTag.objects.get_or_create(name=tag_name)
            post.tags.add(tag_obj)

        # 날짜/시간 합치기
        date_str = request.POST.get('eventDate')
        time_str = request.POST.get('eventTime')
        if date_str and time_str:
            try:
                naive_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                post.event_date = make_aware(naive_dt)
            except ValueError as e:
                print("❌ 날짜 변환 오류:", e)

        post.save()

        # 이미지 추가
        if request.FILES.getlist('images'):
            for f in request.FILES.getlist('images'):
                CompanionImage.objects.create(post=post, image=f)

        return redirect('community:companionview', pk=post.pk)

    return render(request, 'update/comp_update.html', {'post': post})

def updateP(request, pk):
    post = get_object_or_404(ProxyPost, pk=pk)

    if request.method == "POST":
        post.title = request.POST.get('title', post.title)
        post.artist = request.POST.get('artist', post.artist)
        post.category = request.POST.get('category', post.category)
        post.status = request.POST.get('status', post.status)
        post.event_date = request.POST.get('event_date', post.event_date)
        post.location = request.POST.get('location', post.location)
        post.max_people = request.POST.get('max_people', post.max_people)
        post.reward = request.POST.get('reward', post.reward)
        post.description = request.POST.get('description', post.description)
        post.save()
        return redirect('community:proxyview', pk=post.pk)

    return render(request, 'update/proxy_update.html', {'post': post})

def updateSh(request, pk):
    post = get_object_or_404(SharingPost, pk=pk)

    if request.method == "POST":
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        post.artist = request.POST.get('artist', post.artist)
        post.requirement = request.POST.get('requirement', post.requirement)
        post.category = request.POST.get('category', post.category)
        post.type = request.POST.get('type', post.type)
        post.share_date = request.POST.get('share_date', post.share_date)
        post.location = request.POST.get('location', post.location)
        post.status = request.POST.get('status', post.status)
        post.save()
        return redirect('community:sharingview', pk=post.pk)

    return render(request, 'update/shar_update.html', {'post': post})

def updateS(request, pk):
    post = get_object_or_404(StatusPost, pk=pk)

    if request.method == "POST":
        post.title = request.POST.get('title', post.title)
        post.artist = request.POST.get('artist', post.artist)
        post.category = request.POST.get('category', post.category)
        post.status = request.POST.get('status', post.status)
        post.event_date = request.POST.get('event_date', post.event_date)
        post.location = request.POST.get('location', post.location)
        post.max_people = request.POST.get('max_people', post.max_people)
        post.reward = request.POST.get('reward', post.reward)
        post.description = request.POST.get('description', post.description)
        post.save()
        return redirect('community:statusview', pk=post.pk)

    return render(request, 'update/status_update.html', {'post': post})


# 마이페이지 커뮤니티기능 
def mypage_community_list(request):
    if request.method == "GET":
        companion_data = [
            {
                'id': p.id,
                'title': p.title,
                'created_at': p.created_at.strftime("%Y-%m-%d"),
                'views': p.views,
                'comments_count': 0,
            }
            for p in CompanionPost.objects.all()
        ]
        sharing_data = [
            {
                'id': p.id,
                'title': p.title,
                'created_at': p.created_at.strftime("%Y-%m-%d"),
                'views': p.views,
                'comments_count': 0,  #  댓글 모델 없으니 0 고정
            }
            for p in SharingPost.objects.all()
        ]
        proxy_data = [
            {
                'id': p.id,
                'title': p.title,
                'created_at': p.created_at.strftime("%Y-%m-%d"),
                'views': p.views,
                'comments_count': 0,  #  댓글 모델 없으니 0 고정
            }
            for p in ProxyPost.objects.all()
        ]
        status_data = [
            {
                'id': p.id,
                'title': p.title,
                'created_at': p.created_at.strftime("%Y-%m-%d"),
                'views': p.views,
                'comments_count': 0,  #  댓글 모델 없으니 0 고정
            }
            for p in StatusPost.objects.all()
        ]

        return JsonResponse({
            'companion': companion_data,
            'sharing': sharing_data,
            'proxy': proxy_data,
            'shareNow': status_data,
        })
    else:
        return JsonResponse({'error': 'GET only'}, status=405)
    
##### 신고버튼 누르면 신고카운트 db저장 
@require_POST
def report_post(request, post_type, post_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "로그인 필요"}, status=403)

    # 모델 매핑 
    model_map = {
        "companion": CompanionPost,
        "sharing": SharingPost,
        "proxy": ProxyPost,
        "status": StatusPost,
        "review": ExchangeReview, 
    }

    model = model_map.get(post_type)
    if not model:
        return JsonResponse({"error": "잘못된 타입"}, status=400)

    # 게시글 가져오기
    post = get_object_or_404(model, id=post_id)

    #  게시글 신고 수 증가
    post.report_count = (post.report_count or 0) + 1
    post.save()

    #  작성자(User) 신고 수 증가
    author = post.writer if post_type == "review" else post.author
    # 교환후기(ExchangeReview)는 작성자가 writer 필드임을 고려

    if hasattr(author, "report_count"):
        author.report_count = (author.report_count or 0) + 1
        author.save()

    return JsonResponse({
        "status": "ok",
        "post_report_count": post.report_count,
        "user_report_count": author.report_count if hasattr(author, "report_count") else None
    })
    
    


# ===================== 1) 각 게시판 차단/차단해제 API =====================

@require_POST
def toggle_block_companion(request, post_id):
    """동행 게시글 차단/해제 토글"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': '로그인이 필요합니다.'}, status=403)
    user = get_object_or_404(User, user_id=user_id)
    post = get_object_or_404(CompanionPost, id=post_id)

    block, created = BlockedCompanionPost.objects.get_or_create(user=user, post=post)
    if not created:
        block.delete()  # 이미 차단되어있으면 해제
        return JsonResponse({'success': True, 'action': 'unblocked'})
    return JsonResponse({'success': True, 'action': 'blocked'})

@require_POST
def toggle_block_sharing(request, post_id):
    """나눔 게시글 차단/해제 토글"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': '로그인이 필요합니다.'}, status=403)
    user = get_object_or_404(User, user_id=user_id)
    post = get_object_or_404(SharingPost, id=post_id)

    block, created = BlockedSharingPost.objects.get_or_create(user=user, post=post)
    if not created:
        block.delete()
        return JsonResponse({'success': True, 'action': 'unblocked'})
    return JsonResponse({'success': True, 'action': 'blocked'})

@require_POST
def toggle_block_proxy(request, post_id):
    """대리구매 게시글 차단/해제 토글"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': '로그인이 필요합니다.'}, status=403)
    user = get_object_or_404(User, user_id=user_id)
    post = get_object_or_404(ProxyPost, id=post_id)

    block, created = BlockedProxyPost.objects.get_or_create(user=user, post=post)
    if not created:
        block.delete()
        return JsonResponse({'success': True, 'action': 'unblocked'})
    return JsonResponse({'success': True, 'action': 'blocked'})

@require_POST
def toggle_block_status(request, post_id):
    """현황공유 게시글 차단/해제 토글"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': '로그인이 필요합니다.'}, status=403)
    user = get_object_or_404(User, user_id=user_id)
    post = get_object_or_404(StatusPost, id=post_id)

    block, created = BlockedStatusPost.objects.get_or_create(user=user, post=post)
    if not created:
        block.delete()
        return JsonResponse({'success': True, 'action': 'unblocked'})
    return JsonResponse({'success': True, 'action': 'blocked'})

@require_POST
def toggle_block_review(request, post_id):
    """교환후기 게시글 차단/해제 토글"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': '로그인이 필요합니다.'}, status=403)
    user = get_object_or_404(User, user_id=user_id)
    post = get_object_or_404(ExchangeReview, id=post_id)

    block, created = BlockedExchangeReview.objects.get_or_create(user=user, post=post)
    if not created:
        block.delete()
        return JsonResponse({'success': True, 'action': 'unblocked'})
    return JsonResponse({'success': True, 'action': 'blocked'})


# =====================  2) 마이페이지 차단목록 조회 API =====================

@require_GET
def mypage_blocked_list_api(request):
    """마이페이지에서 차단한 게시글 목록 + 블랙리스트 유저 목록 반환"""
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': '로그인이 필요합니다.'}, status=403)
    user = get_object_or_404(User, user_id=user_id)

    # 각 차단 모델에서 차단한 글 목록 가져오기
    blocked_companion = BlockedCompanionPost.objects.filter(user=user).select_related('post')
    blocked_sharing = BlockedSharingPost.objects.filter(user=user).select_related('post')
    blocked_proxy = BlockedProxyPost.objects.filter(user=user).select_related('post')
    blocked_status = BlockedStatusPost.objects.filter(user=user).select_related('post')
    blocked_review = BlockedExchangeReview.objects.filter(user=user).select_related('post')

    # 블랙리스트 유저 (예: 신고수 3회 이상일 경우)
    blacklist_users = User.objects.filter(report_count__gte=3)

    return JsonResponse({
        'success': True,
        'blocked_companion': [
            {'id': b.post.id, 'title': b.post.title, 'author': b.post.author.nickname} for b in blocked_companion
        ],
        'blocked_sharing': [
            {'id': b.post.id, 'title': b.post.title, 'author': b.post.author.nickname} for b in blocked_sharing
        ],
        'blocked_proxy': [
            {'id': b.post.id, 'title': b.post.title, 'author': b.post.author.nickname} for b in blocked_proxy
        ],
        'blocked_status': [
            {'id': b.post.id, 'title': b.post.title, 'author': b.post.author.nickname} for b in blocked_status
        ],
        'blocked_review': [
            {'id': b.post.id, 'title': b.post.title, 'writer': b.post.writer.nickname} for b in blocked_review
        ],
        'blacklist_users': [
            {'id': u.id, 'nickname': u.nickname, 'report_count': u.report_count} for u in blacklist_users
        ]
    })