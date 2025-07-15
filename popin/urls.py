from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('mypage/', include('mypage.urls')),
    path('photocard/', include('photocard.urls')),
    path('signup/', include('signupFT.urls')),
    path('idols/', include('idols.urls')),
    path('login/', include('login.urls')),
    path('adpage/', include('adpage.urls')),
    path('home/', include('home.urls')),
    path('community/', include('community.urls')),
    path('pocadeco/', include('pocadeco.urls')),
    path('customer/', include('customer.urls')),
    
]


# ✅ static()은 따로 추가 (덮어쓰기 X)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns += static(settings.MEDIA_URL, 
                     # document_root=settings.MEDIA_ROOT)

