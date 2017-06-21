from ..models import Category
from ..models import Article,Tag
# register the function as a static tag,
# django can use these tags to render the html
from django import template

from django.db.models.aggregates import Count

register = template.Library()

# after doing this, the function 'get_recent_posts' can be used in html
# function decorator
@register.simple_tag
def get_recent_posts(num=5):
   return Article.objects.all().order_by('-create_time')[:num]

@register.simple_tag
def archives():
    return Article.objects.dates('create_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    category_list = Category.objects.annotate(num_articles = Count('article'))
    #return Category.objects.all()
    return category_list

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)

