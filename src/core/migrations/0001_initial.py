# Generated by Django 4.0.6 on 2022-10-17 23:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=120, verbose_name='地址缩写')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('description', models.CharField(max_length=250, verbose_name='描述')),
                ('order', models.IntegerField(default=0, verbose_name='排序')),
            ],
            options={
                'verbose_name': '日志分类',
                'verbose_name_plural': '日志分类',
                'ordering': ('-order', 'id'),
            },
        ),
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=256, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('is_active', models.BooleanField(default=False)),
                ('gender', models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0, verbose_name='性别')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='最后一次修改时间')),
                ('last_login_time', models.DateTimeField(blank=True, null=True, verbose_name='最后一次登陆时间')),
            ],
            options={
                'verbose_name': '网站用户管理',
                'verbose_name_plural': '网站用户管理',
            },
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='标题')),
                ('sub_title', models.CharField(blank=True, max_length=120, verbose_name='副标题')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
                ('link', models.URLField(blank=True, max_length=120, verbose_name='链接')),
                ('img', models.ImageField(blank=True, upload_to='uploads', verbose_name='图片')),
                ('order', models.IntegerField(default=0, verbose_name='排序')),
            ],
            options={
                'verbose_name': '首页轮播图',
                'verbose_name_plural': '首页轮播图',
                'ordering': ('-order', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, max_length=20, verbose_name='全名')),
                ('title', models.CharField(blank=True, max_length=120, verbose_name='头衔')),
                ('avatar', models.ImageField(default='avatars/login.jpg', upload_to='avatars', verbose_name='头像')),
                ('phone', models.CharField(blank=True, max_length=50, verbose_name='手机')),
                ('wechat', models.CharField(blank=True, max_length=50, verbose_name='微信')),
                ('qq', models.CharField(blank=True, max_length=50, verbose_name='QQ')),
                ('email', models.CharField(blank=True, max_length=120, verbose_name='邮箱')),
                ('url', models.URLField(blank=True, max_length=120, verbose_name='网站')),
                ('github', models.URLField(blank=True, max_length=250, verbose_name='GitHub')),
                ('bio', models.TextField(blank=True, verbose_name='简介')),
                ('hits', models.IntegerField(default=0, verbose_name='浏览量')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '个人资料',
                'verbose_name_plural': '个人资料',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='标题')),
                ('slug', models.SlugField(max_length=120, unique_for_date='created', verbose_name='地址缩写')),
                ('img', models.ImageField(blank=True, null=True, upload_to='uploads', verbose_name='图片')),
                ('summary', models.CharField(blank=True, max_length=250, verbose_name='摘要')),
                ('body', models.TextField(verbose_name='正文')),
                ('views', models.IntegerField(default=0, verbose_name='浏览数')),
                ('flag', models.BooleanField(default=False, verbose_name='标记')),
                ('status', models.CharField(choices=[('draft', '草稿'), ('published', '发布')], default='draft', max_length=120, verbose_name='状态')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='core.category', verbose_name='日志')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '博文日志',
                'verbose_name_plural': '博文日志',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ConfirmString',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, verbose_name='确认码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.siteuser')),
            ],
            options={
                'verbose_name': '邮箱验证码',
                'verbose_name_plural': '邮箱验证码',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='用户名')),
                ('ip', models.CharField(blank=True, max_length=50, verbose_name='Ip')),
                ('body', models.TextField(verbose_name='正文')),
                ('active', models.BooleanField(default=True, verbose_name='有效')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.post', verbose_name='日志')),
            ],
            options={
                'verbose_name': '日志评论',
                'verbose_name_plural': '日志评论',
                'ordering': ('-created',),
            },
        ),
    ]