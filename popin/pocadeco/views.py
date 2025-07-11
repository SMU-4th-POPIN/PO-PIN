from django.shortcuts import render, redirect

from signupFT.models import User
from photocard.models import Photocard
from idols.models import Member
from photocard.models import TempWish
from pocadeco.models import DecoratedPhotocard

from django.db.models import Count
from datetime import date
from django.core.files.base import ContentFile
from django.http import JsonResponse
import json, base64

# 데코포토 전체 리스트
def decolist(request):
    # 전체 데코포토 리스트 불러오기
    decoratedpoca = DecoratedPhotocard.objects.select_related('member__group').order_by('-created_at').annotate(
    wish_count=Count('wished_by_users')
)
    
    # 필터용 쿼리 파라미터 받아오기
    searchgroup = request.GET.getlist('searchgroup')
    selected_members = request.GET.getlist('selectedMembers')
    sort = request.GET.get('sort')
    
    # 조건부 필터링 (값이 있을 경우에만 필터링)
    if searchgroup:
        decoratedpoca = decoratedpoca.filter(member__group__name__in=searchgroup)
        
    # 선택된 멤버가 있으면 필터링
    if selected_members:
        decoratedpoca = decoratedpoca.filter(member__name__in=selected_members)
    # 최신글 순 정렬 옵션 적용
    if sort == 'created_at':
        decoratedpoca = decoratedpoca.annotate('created_at')
    # 좋아요 순 정렬 옵션 적용
    if sort == 'likes':
        decoratedpoca = decoratedpoca.annotate(wish_count=Count('wished_by_users')).order_by('-wish_count')
    # 조회수 정렬 옵션 적용
    elif sort == 'hit':
        decoratedpoca = decoratedpoca.order_by('-hit')
        
    deco_list = []
    for poca in decoratedpoca:
        if poca.tag:  # None이 아니고 빈 문자열도 아님
            tags = poca.tag.split(',')
        else:
            tags = []  # 빈 리스트로 처리
        
        deco_list.append({
            'id': poca.id,
            'title':poca.title,
            'result_image': poca.result_image,
            'user' : poca.user.nickname,
            'created_at': poca.created_at.strftime('%Y-%m-%d'),
            'hit': poca.hit,
            'member': poca.member.name,
            'group': poca.member.group.name,
            'tags': tags,
            'likes': poca.wish_count,
        })
        print(deco_list)

    
    context = {'decoList': deco_list}
    return render(request,'pocadeco/decolist.html', context)

# 데코포카 생성 페이지
def main(request):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        user = User.objects.get(user_id=user_id)
        
        mydeco = DecoratedPhotocard.objects.filter(user=user).order_by('-created_at')
        
        mydecolist = []
        for mypoca in mydeco:
            mydecolist.append({
                'id': mypoca.id,
                'title': mypoca.title,
                'date': mypoca.created_at,
                'result_image':mypoca.result_image,
            })
            
        context = {
            'mydecolist':mydecolist,
        }
        return render(request, 'pocadeco/main.html', context)
    except User.DoesNotExist:
            return redirect('login:main')  # 예외 상황 대비

def mydecolist(request):
    return render(request, 'pocadeco/mydecolist.html')

# 데코포카 상세보기 페이지
def view(reqeust, id):
    decophotocard = DecoratedPhotocard.objects.get(id=id)
    tags = decophotocard.tag.split(',')
    context = {
        'nickname' : decophotocard.user.nickname,
        'title': decophotocard.title,
        'result_image': decophotocard.result_image,
        'tags' : tags,
        'group' : decophotocard.member.group.name,
        'member' :decophotocard.member.name,
        'hit' : decophotocard.hit,
        'like' : decophotocard.wished_by_users.count(),
    }
    return render(reqeust, 'pocadeco/view.html', context)

def save_decopoca(request):
    if request.method == 'POST':
        # 세션에서 user_id 가져오기
        user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

        if not user_id:
            return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return redirect('login:main')  # 예외 상황 대비

        try:
            data = json.loads(request.body)
            
            title = data.get('title')
            image_data = data.get('image')
            group_name = data.get('group')
            member_name = data.get('member')

            if not title or not image_data or not group_name or not member_name:
                return JsonResponse({'status': 'fail', 'reason': '필수 정보 누락'}, status=400)

            # 이미지 처리
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f"{title}.{ext}"
            image_file = ContentFile(base64.b64decode(imgstr), name=file_name)

            # 멤버 찾기
            try:
                member = Member.objects.select_related('group').get(
                    group__name=group_name,
                    name=member_name
                )
            except Member.DoesNotExist:
                return JsonResponse({'status': 'fail', 'reason': '멤버를 찾을 수 없습니다.'}, status=404)

            # 객체 저장
            deco = DecoratedPhotocard.objects.create(
                user=user,
                title=title,
                result_image=image_file,
                member=member
            )

            # 응답 구성
            response_data = {
                'status': 'success',
                'nickname': deco.user.nickname,
                'title': deco.title,
                'result_image': deco.result_image.url,
                'group': deco.member.group.name,
                'member': deco.member.name,
            }
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'fail', 'reason': '허용되지 않은 요청'}, status=405)
def delete_decopoca(request):
    if request.method == 'POST':
        # 세션에서 user_id 가져오기
        user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

        if not user_id:
            return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return redirect('login:main')  # 예외 상황 대비

        try:
            print("접근 시작 ㅎㅎ")
            
            data = json.loads(request.body)
            
            id = data.get('id')

            if not id :
                return JsonResponse({'status': 'fail', 'reason': '필수 정보 누락'}, status=400)
            
            mydeco = DecoratedPhotocard.objects.get(id=id, user=user)
            
            mydeco.delete()
            
            print("완료 ㅎㅎ")

            # 응답 구성
            response_data = {
                'status': 'success',
                'message': "데코포카 " + id + "번 을 삭제했습니다",
            }
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)