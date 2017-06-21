from ..models import Category
from ..models import Article
# register the function as a static tag,
# django can use these tags to render the html
from django import template

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
    return Category.objects.all()

