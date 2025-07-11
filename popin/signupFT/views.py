from django.shortcuts import render,redirect
from idols.models import Group, Member  
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import User
import datetime
from django.http import JsonResponse  # JsonResponse 사용을 위해
from django.views.decorators.csrf import csrf_exempt  # POST 요청 허용
import json  # JSON 파싱용
from django.core.mail import send_mail  # 이메일 전송용
import random

def verify_email_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            input_code = data.get('code')
            input_email = data.get('email')

            saved_code = request.session.get('verification_code')
            saved_email = request.session.get('verification_email')
            print("입력된 코드:", input_code)
            print("세션에 저장된 코드:", saved_code)
            print("입력된 이메일:", input_email)
            print("세션에 저장된 이메일:", saved_email)
            if input_code == saved_code and input_email == saved_email:
                return JsonResponse({'success': True, 'message': '인증 성공'})
            else:
                return JsonResponse({'success': False, 'message': '인증 실패'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'POST 요청이 아닙니다.'})

def send_verification_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'success': False, 'error': '이메일이 없습니다.'})

            # 콘솔에 이메일 보내는 코드 (임시용)
            # send_mail(
            #            '[PO-PIN] 인증 메일',
            #            '이메일 인증을 완료해주세요!',
            #             None,  # None이면 settings.py의 DEFAULT_FROM_EMAIL 사용됨
            #             [email],
            #         )
            #실제로 보내는 코드 
            code = str(random.randint(100000, 999999))
            send_mail(
                        'PO-PIN 이메일 인증',
                         f'인증번호는 {code}입니다.',
                         None,  # settings.py의 DEFAULT_FROM_EMAIL 사용
                         [email],
                         fail_silently=False,
                    )
            request.session['verification_code'] = code
            request.session['verification_email'] = email
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'POST 요청이 아닙니다.'})

def agree(request):
    if request.method == 'POST':
        agree_terms = request.POST.get('agree_terms') == 'on'
        agree_privacy = request.POST.get('agree_privacy') == 'on'
        agree_marketing = request.POST.get('agree_marketing') == 'on'  # 선택 동의는 있어도 되고 없어도 됨

        if not (agree_terms and agree_privacy):
            messages.error(request, "필수 항목에 동의해주세요.")
            return render(request, '1.agree.html')

        # 세션에 마케팅 동의 저장
        request.session['agree_marketing'] = agree_marketing

        return redirect('signup:signup')  # 다음 페이지로
    return render(request, '1.agree.html')



def signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        name = request.POST.get('name')
        birth_date_str = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        nickname=request.POST.get('nickname')
        # 1. 유효성 검사
        if password != confirmPassword:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return render(request, '2.signup.html')

        if User.objects.filter(user_id=user_id).exists():
            messages.error(request, "이미 사용 중인 아이디입니다.")
            return render(request, '2.signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "이미 사용 중인 이메일입니다.")
            return render(request, '2.signup.html')

        # 2. 생년월일 변환
        try:
            birth_date = datetime.datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        except:
            messages.error(request, "생년월일 형식이 올바르지 않습니다.")
            return render(request, '2.signup.html')

        agree_marketing = request.session.get('agree_marketing', False)

        # 3. 유저 생성
        user = User(
            user_id=user_id,
            password=make_password(password),  
            name=name,
            nickname=nickname,
            birth_date=birth_date,
            gender=gender,
            email=email,
            agree_marketing=agree_marketing
        )
        user.save()
        request.session['user_id'] = user.user_id

        return redirect('signup:location_select')

    return render(request, '2.signup.html')


def location_select(request):
    if request.method == 'POST':
        locations = request.POST.get('locations')
        user_id = request.session.get('user_id')



        if user_id and locations:
            try:
                user = User.objects.get(user_id=user_id)
                user.address = locations
                user.save()
                return redirect('signup:member_select')
            except User.DoesNotExist:
            
                messages.error(request, "사용자 정보를 찾을 수 없습니다.")
        else:
        
            messages.error(request, "장소 선택 저장에 실패했습니다.")
    return render(request, '3.location_select.html')

def member_select(request):
    if request.method == 'POST':
        group_names = request.POST.getlist('group_name')  # 수정 확인
        member_names = request.POST.getlist('member_name')  # 수정 확인
        user_id = request.session.get('user_id')

        if user_id and group_names and member_names:
            try:
                user = User.objects.get(user_id=user_id)
                group_queryset_list = Group.objects.filter(name__in=group_names)
                member_queryset_list = Member.objects.filter(name__in=member_names, group__in=group_queryset_list)

                user.bias_group.set(group_queryset_list)
                user.bias_member.set(member_queryset_list)
                user.save()

                return redirect('signup:completed')  
            except (User.DoesNotExist, Group.DoesNotExist, Member.DoesNotExist) as e:
                messages.error(request, "선택한 정보 저장에 실패했습니다.")
        else:
            messages.error(request, "최애 그룹과 멤버를 선택해주세요.")

    return render(request, '4.member_select.html')

def completed(request):
    return render(request, '5.completed.html')