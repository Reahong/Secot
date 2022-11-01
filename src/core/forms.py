from django import forms
from django.core import validators
from .models import Comment


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名', required=True, min_length=2, max_length=128)
    password = forms.CharField(
        label='密码', required=True, min_length=2, max_length=10)


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", required=True, max_length=128)
    password1 = forms.CharField(label="密码", max_length=256, required=True)
    password2 = forms.CharField(label="确认密码", required=True, max_length=256)
    email = forms.EmailField(label="邮箱地址")

# 手动声明表单类


# class CommentForm(forms.Form):
#     name = forms.CharField(max_length=50, label="姓名", validators=[
#                            validators.MinLengthValidator(2, '姓名长度不得少于2个字符')])
#     body = forms.CharField(label="正文")


class CommentForm(forms.ModelForm):
    """根据数据模型生成表单"""

    class Meta:
        model = Comment
        fields = ('name', 'body',)

        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'border rounded-md p-2 text-sm',
                'placeholder': '姓名'
            }),
            "body": forms.Textarea(attrs={
                'class': 'w-full border rounded-md p-2 text-sm',
                'rows': 3,
                'placeholder': '留下您的评论...'
            }),
        }
