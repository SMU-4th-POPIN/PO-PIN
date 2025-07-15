from django.contrib import admin
from .models import ProxyPost,ProxyTag,ProxyImage
from .models import  ProxyComment
from .models import CompanionPost,CompanionTag,CompanionImage
from .models import CompanionComment
from .models import SharingPost, SharingTag, SharingImage
from .models import ExchangeReview, ReviewImage, ReviewTag
from .models import StatusPost, StatusTag, StatusImage
from django.forms import BaseInlineFormSet, ValidationError


### 이미지 개수 제한용 FormSet
# class LimitedImageInlineFormSet(BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#         total_forms = len([
#             form for form in self.forms
#             if not form.cleaned_data.get('DELETE', False) and form.cleaned_data
#         ])
#         #  pk 존재할 때만 이미지 개수 체크
#         if self.instance.pk and self.instance.images.count() + total_forms > 5:
#             raise ValidationError('이미지는 최대 5개까지만 등록할 수 있습니다.')
class LimitedImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # 삭제 요청 제외한 신규 업로드 수
        new_uploads = len([
            form for form in self.forms
            if not form.cleaned_data.get('DELETE', False)
            and not form.instance.pk  # pk 없으면 신규 이미지
        ])

        # 현재 저장된 이미지 수
        existing_count = self.instance.images.count() if self.instance.pk else 0

        if existing_count + new_uploads > 5:
            raise ValidationError('이미지는 최대 5개까지만 등록할 수 있습니다.')
# 이미지 인라인
class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1
    readonly_fields = ['uploaded_at']
    formset = LimitedImageInlineFormSet
    
# 후기 리뷰 어드민
@admin.register(ExchangeReview)
class ExchangeReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "writer", "partner", "overall_score", "method", "created_at", "views")
    list_filter = ("method", "created_at")
    #search_fields = ("title", "content", "writer__username", "partner__username", "artist")
    inlines = [ReviewImageInline]
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at", "views")

# 태그 어드민
@admin.register(ReviewTag)
class ReviewTagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    #search_fields = ("name",)

# 이미지 어드민
@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ("review", "image")
    readonly_fields = ("uploaded_at",)

###################################################################################################################


# ### 이미지 개수 제한용 FormSet
# class LimitedImageInlineFormSet(BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#         total_forms = len([form for form in self.forms if not form.cleaned_data.get('DELETE', False) and form.cleaned_data])
#         if self.instance.images.count() + total_forms > 5:
#             raise ValidationError('이미지는 최대 5개까지만 등록할 수 있습니다.')
        
# 이미지 인라인
class CompanionImageInline(admin.TabularInline):
    model = CompanionImage
    extra = 1
    readonly_fields = ['uploaded_at']
    formset = LimitedImageInlineFormSet

@admin.register(CompanionImage)
class CompanionImageAdmin(admin.ModelAdmin):
    list_display = ("post", "image", "uploaded_at")
    readonly_fields = ("uploaded_at",)
    
@admin.register(CompanionTag)
class CompanionTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    #search_fields = ('name',)
    
@admin.register(CompanionPost)
class CompanionPostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'artist',
        'category',
        'event_date',
        'location',
        'max_people',
        'status',
        'created_at',
        'views',
    )
    list_filter = ('category', 'status', 'created_at')
    # search_fields = ('title', 'content', 'artist', 'location', 'author__user_id','participants__user_id')  
    # autocomplete_fields = ('author', 'participants')
    readonly_fields = ('created_at', 'views')

@admin.register(CompanionComment)
class CompanionCommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'content',
        'created_at',
    )
    # search_fields = ('post__title', 'content')
    # autocomplete_fields = ["post"]  
    readonly_fields = ('created_at',)

###########################################################################################

# # 최대 5장 제한용 FormSet
# class LimitedImageInlineFormSet(BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#         total_forms = len([
#             form for form in self.forms
#             if not form.cleaned_data.get('DELETE', False) and form.cleaned_data
#         ])
#         if self.instance.images.count() + total_forms > 5:
#             raise ValidationError('이미지는 최대 5개까지만 등록할 수 있습니다.')
# 이미지 인라인

class ProxyImageInline(admin.TabularInline):
    model = ProxyImage
    extra = 1
    formset = LimitedImageInlineFormSet
    readonly_fields = ['uploaded_at']
    from .models import ProxyImage

@admin.register(ProxyImage)
class ProxyImageAdmin(admin.ModelAdmin):
    list_display = ("post", "image","uploaded_at")
    readonly_fields = ("uploaded_at",)
    
#태그
@admin.register(ProxyTag)
class ProxyTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    #search_fields = ('name',)
    
@admin.register(ProxyPost)
class ProxyPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category', 'status', 'author', 'created_at', 'views')
    list_filter = ('category', 'status', 'created_at')
    #search_fields = ('title', 'artist', 'description', 'location')
    readonly_fields = ('created_at', 'views', 'comments_count')

@admin.register(ProxyComment)
class ProxyCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    #search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at',)

##################################################

@admin.register(SharingTag)
class SharingTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    #search_fields = ['name']
    
# ### 이미지 개수 제한용 FormSet
# class LimitedImageInlineFormSet(BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#         total_forms = len([
#             form for form in self.forms
#             if not form.cleaned_data.get('DELETE', False) and form.cleaned_data
#         ])
#         if self.instance.images.count() + total_forms > 5:
#             raise ValidationError('이미지는 최대 5개까지만 등록할 수 있습니다.')

class SharingImageInline(admin.TabularInline):  # 이미지 인라인으로 등록
    model = SharingImage
    extra = 1
    readonly_fields = ['uploaded_at']
    formset = LimitedImageInlineFormSet

@admin.register(SharingPost)
class SharingPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'type', 'share_date', 'location', 'created_at', 'views']
    list_filter = ['category', 'type', 'share_date']
    #search_fields = ['title', 'content', 'author__username', 'tags__name']
    readonly_fields = ['views', 'created_at']
    inlines = [SharingImageInline]
    filter_horizontal = ['tags']  # 태그 다중 선택 UI


@admin.register(SharingImage)
class SharingImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'uploaded_at']
    readonly_fields = ['uploaded_at']

##################################################################

class StatusImageInline(admin.TabularInline):  # 이미지 인라인으로 등록
    model = StatusImage
    extra = 1
    readonly_fields = ['uploaded_at']
    formset = LimitedImageInlineFormSet

@admin.register(StatusPost)
class StatusPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'event_datetime','created_at', 'views'] 
    readonly_fields = ['views', 'created_at']
    inlines = [StatusImageInline]
    filter_horizontal = ['tags']  # 태그 다중 선택 UI


@admin.register(StatusImage)
class StatusImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'uploaded_at']
    readonly_fields = ['uploaded_at']
