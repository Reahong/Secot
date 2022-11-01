import ssl
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from core.models import *
from . import models
from django.core.mail import send_mail
from core.forms import LoginForm, RegisterForm, CommentForm
from core.utils import hash_code
from Blog import settings
import datetime
import requests
from taggit.models import Tag
# Create your views here.


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email, code):

    # 发送邮件
    subject = '欢迎注册RE的个人网站！'

    message = '''
       欢迎注册RE的个人网站,亲爱的用户请点击链接激活账户吧！

                   <br> <a href='http://127.0.0.1:8000/confirm/{}'>点击激活</a>
                   <br>
                   <p>此链接有效期{}天</p>
                   <br>

                   &emsp;&emsp; &emsp; &emsp; &emsp; &emsp;&emsp; &emsp; &emsp; &emsp; &emsp;&emsp; &emsp; &emsp; &emsp; &emsp;&emsp; &emsp; &emsp; &emsp; RE.

                   '''.format(code, settings.CONFIRM_DAYS)

    result = send_mail(subject, message, settings.EMAIL_HOST_USER, [
                       email, ], html_message=message)
    print(result)


def index(request):
    # items = Post.objects.filter(status ='published')[:10]
    items = Post.published.all()[:10]
    slides = Slide.objects.all()
    return render(request, 'index.html',
                  {"items": items,

                   "slides": slides,

                   })


def posts(request):
    items = Post.published.all()
    # 按标签分类 过滤
    tag = request.GET.get('tag', None)
    cat = request.GET.get('cat', None)
    if tag:
        tag_obj = Tag.objects.get(slug=tag)
        items = items.filter(tags__in=[tag_obj])
    if cat:
        items = items.filter(category__id=cat)

    paginator = Paginator(items, 10)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    # categories = Category.objects.all()
    return render(request, 'post-list.html', {
        "items": items,
        # "categories": categories,
    })


def details(request, slug):

    item = Post.objects.get(slug=slug)
    item.views += 1
    item.save()
    form = CommentForm()
    # tags = item.tags.split(',')
    try:
        prev_post = item.get_next_by_created()
    except Post.DoesNotExist:
        prev_post = None

    try:
        next_post = item.get_previous_by_created()
    except Post.DoesNotExist:
        next_post = None

    if request.method == 'POST':
        # 手动获取表单数据
        # name = request.POST.get('name', None)
        # body = request.POST.get('body', None)
        # if name and body:
        #     comment = Comment()
        #     comment.post = item
        #     comment.name = name
        #     comment.body = body
        #     comment.ip = get_client_ip(request)
        #     comment.save()
        # 从CommentForm 实例中获取数据
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = item
            comment.ip = get_client_ip(request)
            comment.save()

        return redirect(item)

    return render(request, 'details.html',
                  {
                      'item': item,
                      'form': form,
                      # 'tags': tags,
                      'prev_post': prev_post,
                      'next_post': next_post})


def post_search(request):
    items = Post.published.all()
    q = request.GET.get('q', None)
    if q.strip():
        items = items.filter(title__contains=q)
    else:
        return redirect(reverse('posts'))
    paginator = Paginator(items, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "post-search.html",

                  {"items": posts,
                   "page": page,
                   })


def get_client_ip(request):
    """ 获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    r = requests.get(
        'https://api.ip138.com/ip/?ip=%s&datatype=jsonp&token=3a43af4d7d8dfc9e2f773ec56165c26a' % ip)
    if r.json()['ret'] == 'ok':
        i = r.json()['data']
        country = i[0]
        province = i[1]
        city = i[2]
        checkip = country + ' ' + province + ' ' + city

    else:
        print('未查到归属地')

    return checkip


def about(request):
    item = Profile.objects.get(id=1)
    item.hits += 1
    item.save()
    return render(request, 'about.html', {"item": item})


def login(request):

    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.SiteUser.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login.html', {'message': message})

            if not user.is_active:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login.html', {'message': message})

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['username'] = user.name
                return redirect('/')
            else:
                message = '密码不正确！'
                return render(request, 'login.html', {'message': message})
        else:
            return render(request, 'llogin.html')

    login_form = LoginForm()
    return render(request, 'login.html')


def register(request):
    # 如果用户已经登陆，则不能注册跳转到首页
    if request.session.get('is_login', None):
        return redirect('/')
    # 如果是post请求
    if request.method == 'POST':
        print(request.POST)
        register_from = RegisterForm(request.POST)
        message = '请检查填写的内容！'
        # 先校验提交的数据是否通过
        if register_from.is_valid():
            # 清洗数据
            username = register_from.cleaned_data.get('username')
            password1 = register_from.cleaned_data.get('password1')
            password2 = register_from.cleaned_data.get('password2')
            email = register_from.cleaned_data.get('email')

            # 接下来判断用户和邮箱是否被注册
            same_name_user = SiteUser.objects.filter(name=username)
            print(same_name_user)
            if same_name_user:
                message = '用户已存在！'
                return render(request, 'register.html',  {'message': message})
            same_email_user = SiteUser.objects.filter(email=email)
            if same_email_user:
                message = '邮箱已存在！'
                return render(request, 'register.html',)

            try:
                # 将注册的信息存储到数据库
                new_user = SiteUser(
                    name=username, password=hash_code(password1), email=email)
                new_user.save()

                # 生成确认码

                code = make_confirm_string(new_user)
                send_email(email, code)
                message = '注册成功！请前往邮箱进行确认！'

            except Exception as e:
                new_user.delete()
                message = '发送邮件失败！'
                print(e)
                return render(request, 'register.html')
            else:
                return render(request, 'register.html', locals())
    # 如果是get请求 返回用户注册的HTML界面
    register_from = RegisterForm()
    return render(request, 'register.html', locals())


def user_confirm(request, code):

    print("code:", code)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)

    except:
        message = '无效的确认请求！'
        return render(request, 'confirm.html',  {'message': message})
    create_time = confirm.create_time
    now = datetime.datetime.now()
    if now > create_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册！'
        return render(request, 'confirm.html', {'message': message})
    else:
        confirm.user.is_active = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认！请使用账户登陆！'
        return render(request, 'confirm.html',  {'message': message})


def logout(request):
    if request.session.get('is_login'):
        request.session.flush()
    return redirect('login')


def comment_control(request):
    if request.session.username:
        body = request.POST.get('body')
