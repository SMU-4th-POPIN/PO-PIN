
from django.shortcuts import render,redirect
from signupFT.models import User
from photocard.models import Photocard
from django.db.models import Count
from django.core.paginator import Paginator


def main(request):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        user = User.objects.get(user_id=user_id) # 로그인한 사용자
        
        # 전체 게시글
        total_photocard = Photocard.objects.all().count() 
        # 활성 사용자
        total_user = User.objects.all().count() 
        # 교환 완료
        completed_photocard = Photocard.objects.filter(sell_state='후', buy_state='후').count() 
        
        # 최근 인기 포토카드 (거래중인 것)
        photocards = Photocard.objects.filter(sell_state='중', buy_state=None).select_related('member__group').annotate(
        wish_count=Count('wished_by_users')).order_by('-wish_count')[:4]
        # 최신 게시글
        recent = Photocard.objects.filter(sell_state='중', buy_state=None).order_by('-created_at')[:5]
        
        context = {
            'username': user.name or user.nickname or user.user_id,  # 로그인한 사용자
            'photocards': photocards, # 최근 인기 포토카드
            'total_photocard':total_photocard, # 전체 게시글
            'total_user':total_user,  # 활성 사용자
            'completed_photocard':completed_photocard, #교환 완료
            'recent':recent
        }
        
        return render(request, 'main.html', context)
    
    except User.DoesNotExist:
        return redirect('login:main')  # 예외 상황 대비
    
    

def recent(request):
    posts = Photocard.objects.all().order_by('-created_at')
        
    # GET 요청에서 카테고리와 검색어를 받음
    category = request.GET.get('category', '전체')  # 기본값은 '전체'
    searchinput = request.GET.get('searchinput', '')

    # 카테고리 필터링
    if category == '교환':
        filtered_posts = Photocard.objects.filter(trade_type='교환').order_by('-created_at')
    elif category == '판매':
        filtered_posts = Photocard.objects.filter(trade_type='판매').order_by('-created_at')
    else:
        filtered_posts = posts  # '전체'일때 모든 게시글을 표시

    # 검색어 필터링
    if searchinput:
        filtered_posts = filtered_posts.filter(title__icontains=searchinput)
    
    # 페이지네이터
    paginator = Paginator(filtered_posts, 5)
    page = int(request.GET.get('page', 1))
    page_num = paginator.get_page(page)

    return render(request, 'recent.html', {'category':category, 'searchinput':searchinput, 'page_num':page_num})