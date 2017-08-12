from django import template
from ..models import Post,Category
from django.db.models.aggregates import Count
from myblog.models import Category

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    # 别忘了在顶部引入 Category 类
    category_list = Category.objects.annotate(num_posts = Count('post'))
    #return Category.objects.all()
    return category_list