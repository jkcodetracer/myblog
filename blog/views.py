from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article, Category

# support markdown
import markdown

# Create your views here.
def index(request):
    articles = Article.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context = {
        'article_list' : articles
        })

def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
    return render(request, 'blog/detail.html', context={'post':article})

def archives(request, year, month):
    article_list = Article.objects.filter(create_time__year = year,
                                          create_time__month = month).order_by('-create_time')
    return render(request, 'blog/index.html', context={'article_list':article_list})

def categories(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    article_list = Article.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog/index.html', context={'article_list':article_list})

