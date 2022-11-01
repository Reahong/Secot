from codecs import register
import re
from django import template
from taggit.models import Tag
from ..models import Post
from django.db.models import Count

register = template.Library()

# 定义为转换字符串的过滤器


@register.filter(name="to_str")
def to_str(value):
    return str(value)


# 高亮选择搜索结果关键字
@register.filter(name="highlight")
def highlight(text, search):
    if search:
        text = text.replace(
            search, f'<span class="bg-blog-dary text-white">{search}</span>')
        return text


# 定义并注册“包含标签”(所有日志标签)
@register.inclusion_tag('core/tags.html')
def display_tags():
    tags = Tag.objects.all()
    return {"tags": tags}


# 定义并注册标签 (热门文章 -日志评论最多的前N条)
@register.inclusion_tag('core/popular-posts.html')
def display_most_commented_posts(count=5):
    items = Post.published.annotate(total_comments=Count(
        'comments')).order_by('-total_comments')[:count]
    return {"popular_posts": items}


# 心知天气 API
@register.inclusion_tag('core/weather.html')
def weather():
    result = {
        'city': '武汉',
        'text': '未知',
        'temperature': '未知'
    }
    import requests
    from Blog.settings import WEATHER_API_URL, WEATHER_API_KEY, WEATHER_CITY
    payload = {
        'key': WEATHER_API_KEY,
        'location': WEATHER_CITY,
    }
    r = requests.get(WEATHER_API_URL, params=payload)
    if r.status_code == 200:
        data = r.json()
        result['city'] = data['results'][0]['location']['name']
        result['text'] = data['results'][0]['now']['text']
        result['temperature'] = data['results'][0].get(
            'now').get('temperature')
    return result
