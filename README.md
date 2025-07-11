# PO-PIN
<p>SMU-engineer 4th Project Team 1</p>
<br>

## 협업 방식
***

    feat : 새로운 기능 추가
    fix : 버그 수정
    hotfix : 급한 버그 수정
    docs : 문서 수정
    style : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
    refactor : 코드 리펙토링
    test : 테스트 코드, 리펙토링 테스트 코드 추가
    chore : 빌드 업무 수정, 패키지 매니저 수정


    ex: feature branch : 새로운 기능을 제작할 때 생성해주세요. 
    로그인 파트 제작을 진행하시면 feat/login
    ex: fix branch: 버그를 수정할 때 생성해주세요. 
    로그인 파트 버그를 수정할때는 fix/login


본인 branch에 작업을 진행하고, main branch에 PR(Pull Request)를 날리고, 팀원에게 말씀해주세요. 팀원들이 상호 보완하면서 개선해나가면 되겠습니다.


항상 첫 작업을 시작하기 전에, main branch를 Pull 받고 시작해주세요!


### Django 스타일 가이드
***

| 항목           | 스타일                    | 예시                                      |
|----------------|---------------------------|-------------------------------------------|
| 모델 클래스명  | `PascalCase`              | `TradePost`, `UserProfile`                |
| 필드/변수명     | `snake_case`              | `created_at`, `user_name`, `status_code`  |
| 상수           | `UPPER_SNAKE_CASE`        | `STATUS_CHOICES`, `DEFAULT_TIMEOUT`       |

