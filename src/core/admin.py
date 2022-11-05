from django.contrib import admin
from django import forms
from .models import Profile, Category, Post, SiteUser, ConfirmString, Comment, Slide
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

# Register your models here.
admin.site.site_header = '阿红个人博客管理后台'
admin.site.site_title = '阿红个人博客管理后台'
admin.site.index_title = '阿红个人博客管理后台'


class PorfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'title', 'phone', 'created')
    ordering = ('-created',)


admin.site.register(Profile, PorfileAdmin)

# 自定义表单管理


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": forms.Textarea
        }

# 注册类别管理


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_title', 'link', 'order')
    link_field = ('title',)
    list_editable = ('order',)
    ordering = ('-order', 'id')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('slug', 'name', 'order')
    list_editable = ('order',)


# 日志管理表单
class PostAdminForm(forms.ModelForm):
    class Meta:
        models = Post
        fields = "__all__"
        widgets = {
            'summary': forms.Textarea,
            'body': SummernoteWidget()
        }

# 日志后台管理


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'slug', 'category', 'views', 'flag', 'status')
    search_fields = ("title", "body")
    list_filter = ('category', 'flag', 'status')
    date_hierarchy = 'created'
    ordering = ('-created', 'status')

# 注册评论管理


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'active', 'created')
    list_filter = ('active', 'created')
    ordering = ('-created',)


class SiteUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'email', 'is_active']
    list_display_links = ['name']
    list_filter = ['gender', 'create_time']
    list_per_page = 10


class ConfirmStringAdmin(admin.ModelAdmin):
    list_display = ('code',)


admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(ConfirmString, ConfirmStringAdmin)
