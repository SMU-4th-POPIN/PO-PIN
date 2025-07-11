from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import ExchangeReview, ReviewImage, ReviewTag
from .models import ExchangeReview
from .models import SharingPost, SharingTag, SharingImage


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






##### 커뮤니티
# 메인페이지
def main(request):
    return render(request, 'community/main.html')

User = get_user_model()


@login_required
def write_review(request):
    if request.method == "POST":
        print("📥 요청 방식:", request.method)
        print("📥 POST 데이터:", request.POST)
        print("📥 FILES:", request.FILES)
        
   # 1. 입력값 받기
        user = request.user
        title = request.POST.get('title', '').strip()
        artist = request.POST.get('artist', '').strip()
        content = request.POST.get('content', '').strip()
        partner_username = request.POST.get('partner', '').strip()
        tag_string = request.POST.get('tags', '').strip()
        method = request.POST.get('method', '').strip()
        transaction_type = request.POST.get('transaction_type', '').strip() 
        overall_score = request.POST.get('overall_score')
        images = request.FILES.getlist('images')
        print("✅ 저장 직전: ", title, content, overall_score, user.username)
        
        # 2. 필수값 체크
        required_fields = {
            "제목": title,
            "내용": content,
            "교환 방식": method,
            "총 평점": overall_score,
        }
        for label, value in required_fields.items():
            if not value:
                return render(request, 'community_write_review.html', {
                    "error": f"{label}은(는) 필수 항목입니다.",
                    "form_data": request.POST
                })

        # 3. 유효한 파트너 유저 찾기
        try:
            partner_user = User.objects.get(user_id=partner_username)
            print("파트너 유저 확인:", partner_user.username)
        except User.DoesNotExist:
            print(" 파트너 유저 없음:", partner_username)  # ← 이거 찍히면 문제
            return render(request, 'community/community_write_review.html', {
                "error": "입력한 교환 상대방 아이디가 존재하지 않습니다.",
                "form_data": request.POST
            })

        # 4. 정수 변환
        try:
            overall_score = int(overall_score)
        except ValueError:
            return render(request, 'community/community_write_review.html', {
                "error": "총 평점은 숫자여야 합니다.",
                "form_data": request.POST
            })

        # 5. 리뷰 저장
        try:
            review = ExchangeReview.objects.create(
                title=title,
                content=content,
                artist=artist,
                method=method,
                transaction_type=transaction_type,
                overall_score=overall_score,
                writer=user,
                partner=partner_user
            )
            print(" 리뷰 생성 완료:", review.id)
        except Exception as e:
            print(" 리뷰 저장 실패:", e)
            return render(request, 'community/community_write_review.html', {
                "error": f"리뷰 저장 중 오류 발생: {str(e)}",
                "form_data": request.POST
            })

        # 6. 태그 저장
        if tag_string:
            tag_names = tag_string.replace(",", " ").split()
            for tag_name in tag_names:
                tag_obj, _ = ReviewTag.objects.get_or_create(name=tag_name)
                review.tags.add(tag_obj)
            print(" 태그 추가:", tag_names)

        # 7. 이미지 수 제한 확인
        if len(images) > 5:
            return render(request, 'community/community_write_review.html', {
                "error": "이미지는 최대 5개까지만 업로드할 수 있습니다.",
                "form_data": request.POST
            })

        # 8. 이미지 저장
        for img in images: 
            try:
                 ReviewImage.objects.create(review=review, image=img)
                 print(" 이미지 저장됨:", img.name)
            except Exception as e: 
                print(" 이미지 저장 실패 :" ,  e)

        return redirect('chgReview:main')  # 또는 너의 리뷰 리스트 페이지

    # GET 요청일 경우
    return render(request, 'community/community_write_review.html')

# 최근게시글
def recent(request):
    return render(request, 'community/community_recent.html')

# 동행모집글 작성
def write_companion(request):
    return render(request, 'community/community_write_companion.html')

# 대리구매글 작성
def write_proxy(request):
    return render(request, 'community/community_write_proxy.html')

# 후기 작성
def write_review(request):
    return render(request, 'community/community_write_review.html')

# 나눔글 작성
def write_sharing(request):
    return render(request, 'community/community_write_sharing.html')

# 현황공유 작성
def write_status(request):
    return render(request, 'community/community_write_status.html')

##### 교환/판매후기 게시판
def chgReview(request) :
    return render(request,'chgReview/main.html')

def chgReviewmain(request):
    reviews = ExchangeReview.objects.all().order_by('-created_at')  # 최신순
    return render(request, 'chgReview/main.html', {'reviews': reviews})

def chgReviewview(request) :
    return render(request,"chgReview/chgR_view.html")




##### 동행 게시판
def companion(request) :
    return render(request,'companion/main.html')

##### 대리구매 게시판
def proxy(request) :
    return render(request,'proxy/main.html')

##### 나눔 게시판
def sharing(request) :
    return render(request,'sharing/main.html')

##### 현황공유 게시판
def status(request) :
    return render(request,'status/main.html')


def write_sharing(request):
     if request.method == "POST":
        user = request.user
        title = request.POST.get('title', '').strip()
        artist = request.POST.get('artist', '').strip()
        category =request.POST.get('category', '').strip()
        location= request.POST.get('location','').strip()
        share_date=request.POST.get('share_date','').strip()
        requirement=request.POST.get('requirement','').strip()
        content = request.POST.get('content', '').strip()
        tag_string = request.POST.get('tags', '').strip()
        images = request.FILES.getlist('images')
        # 2. 필수값 체크
        required_fields = {
            "제목": title,
            "내용": content,
            "장소": location,
            "필수사항": requirement,
        }
        for label, value in required_fields.items():
            if not value:
                return render(request, 'community_write_sharing.html', {
                    "error": f"{label}은(는) 필수 항목입니다.",
                    "form_data": request.POST
                })


        # 3. 나눔글 저장
        try:
            post = SharingPost.objects.create(
                title=title,
                artist=artist,
                category =category,
                location=location,
                share_date =share_date ,
                content=content,
                author=user,
               
            )
            print(" 리뷰 생성 완료:", post.id)
        except Exception as e:
            print(" 리뷰 저장 실패:", e)
            return render(request, 'community_write_sharing.html', {
                "error": f"리뷰 저장 중 오류 발생: {str(e)}",
                "form_data": request.POST
            })

        # 4. 태그 저장
        if tag_string:
            tag_names = tag_string.replace(",", " ").split()
            for tag_name in tag_names:
                tag_obj, _ = SharingTag.objects.get_or_create(name=tag_name)
                post.tags.add(tag_obj)
            print(" 태그 추가:", tag_names)

        # 5. 이미지 수 제한 확인
        if len(images) > 5:
            return render(request, 'community_write_sharing.html', {
                "error": "이미지는 최대 5개까지만 업로드할 수 있습니다.",
                "form_data": request.POST
            })

        # 6. 이미지 저장
        for img in images: 
            try:
                 SharingImage.objects.create(post=post, image=img)
                 print(" 이미지 저장됨:", img.name)
            except Exception as e: 
                print(" 이미지 저장 실패 :" ,  e)

        return redirect('sharing:main')  # 또는 너의 리뷰 리스트 페이지
    
     return render(request, 'community/community_write_sharing.html')
