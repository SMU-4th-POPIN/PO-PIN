
from django.shortcuts import render,redirect

from signupFT.models import User
from photocard.models import Photocard
from pocadeco.models import DecoratedPhotocard
from adpage.models import Notice

from django.db.models import Count
from django.core.paginator import Paginator
import json


def main(request):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        user = User.objects.get(user_id=user_id) # 로그인한 사용자
        
        # 공지사항 최신글 (임시)
        notices = Notice.objects.all().order_by('is_pinned','-created_at')[:4]
        notice_titles = [notice.title for notice in notices]
        
        # 전체 게시글
        total_photocard = Photocard.objects.all().count() 
        # 활성 사용자
        total_user = User.objects.filter(state=1).count()
        # 교환 완료
        completed_photocard = Photocard.objects.filter(sell_state='후', buy_state='후').count() 
        # 포카 꾸미기
        total_decopoca = DecoratedPhotocard.objects.all().count()
        
        # 최근 인기 포토카드 (거래중인 것)
        photocards = Photocard.objects.filter(sell_state='중', buy_state=None).select_related('member__group').annotate(
        wish_count=Count('wished_by_users')).order_by('-wish_count')[:4]
        
        # 교환 최신 게시글
        recent_exchange = Photocard.objects.filter(
            sell_state='중',
            buy_state=None,
            trade_type='교환'
        ).order_by('-created_at').first()

        # 판매 최신 게시글
        recent_sale = Photocard.objects.filter(
            sell_state='중',
            buy_state=None,
            trade_type='판매'
        ).order_by('-created_at').first()
        
        recent_deco = DecoratedPhotocard.objects.all().order_by('-created_at').first()

        # None이 아닌 경우만 리스트에 추가
        recent = []
        if recent_exchange:
            recent.append({
                'id': recent_exchange.pno,
                'category': recent_exchange.trade_type,
                'title': recent_exchange.title,
                'user': recent_exchange.seller.nickname,
                'created_at' : recent_exchange.created_at,
                'hit' : recent_exchange.hit,
            })
            
        if recent_sale:
            recent.append({
                'id': recent_sale.pno,
                'category': recent_sale.trade_type,
                'title': recent_sale.title,
                'user': recent_sale.seller.nickname,
                'created_at' : recent_sale.created_at,
                'hit' : recent_sale.hit,
            })
        if recent_deco:
            recent.append({
                'id': recent_deco.id,
                'category': "포카 꾸미기",
                'title': recent_deco.title,
                'user': recent_deco.user.nickname,
                'created_at' : recent_deco.created_at,
                'hit' : recent_deco.hit,
            })
            
        context = {
            'username': user.name or user.nickname or user.user_id,  # 로그인한 사용자
            'photocards': photocards, # 최근 인기 포토카드
            'total_photocard':total_photocard, # 전체 게시글
            'total_user':total_user,  # 활성 사용자
            'completed_photocard':completed_photocard, #교환 완료
            'total_decopoca':total_decopoca,
            'recent':recent,
            'titles': json.dumps(notice_titles),
        }
        
        return render(request, 'main.html', context)
    
    except User.DoesNotExist:
        return redirect('login:main')  # 예외 상황 대비

def recent(request):
    posts = []
    photocards = Photocard.objects.all().order_by('-created_at')
    decophotocards = DecoratedPhotocard.objects.all().order_by('-created_at')
    
    for photocard in photocards :
        posts.append({
            'id': photocard.pno,
            'category': photocard.trade_type,
            'title': photocard.title,
            'user': photocard.seller.nickname,
            'created_at' : photocard.created_at,
            'hit' : photocard.hit,
        })
        
    for decopoca in decophotocards:
        posts.append({
            'id': decopoca.id,
            'category': "포카 꾸미기",
            'title': decopoca.title,
            'user': decopoca.user.nickname,
            'created_at' : decopoca.created_at,
            'hit' : decopoca.hit,
        })
        
        
    # created_at 기준 최신순 정렬
    posts.sort(key=lambda x: x['created_at'], reverse=True)
    
        
    # GET 요청에서 카테고리와 검색어를 받음
    category = request.GET.get('category', '전체')  # 기본값은 '전체'
    searchinput = request.GET.get('searchinput', '')

    # 카테고리 필터링
    if category == '교환':
        filtered_posts = [p for p in posts if p['category'] == '교환']
    elif category == '판매':
        filtered_posts = [p for p in posts if p['category'] == '판매']
    elif category == '포카 꾸미기':
        filtered_posts = [p for p in posts if p['category'] == '포카 꾸미기']
    else:
        filtered_posts = posts  # '전체'일때 모든 게시글을 표시

    # 검색어 필터링
    if searchinput:
        filtered_posts = [p for p in filtered_posts if searchinput.lower() in p['title'].lower()]
    
    # 페이지네이터
    paginator = Paginator(filtered_posts, 5)
    page = int(request.GET.get('page', 1))
    page_num = paginator.get_page(page)

    return render(request, 'recent.html', {'category':category, 'searchinput':searchinput, 'page_num':page_num})