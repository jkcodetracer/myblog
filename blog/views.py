from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article, Category, Tag

from comments.forms import CommentForm

# support markdown
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# use ListView to do paginate
from django.views.generic.list import ListView

# Create your views here.
def index(request):
    articles = Article.objects.all()
    # '5' articles per page
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context = {
        'article_list' : articles
        })

# show articles belongs to a tag
class TagView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags = tag)

# a better pagination
class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # fetch the original context
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.extra_pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)

        return context

    def extra_pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        current_page = page.number
        total_pages = paginator.num_pages
        # [1,2,3,4,5] page index
        page_range = paginator.page_range

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        right = page_range[current_page:
                               (current_page+2) if (current_page+2) < total_pages else total_pages]
        if len(right) > 0 and right[-1] < total_pages - 1:
            right_has_more = True
        if len(right) > 0 and right[-1] < total_pages:
            last = True

        left = page_range[(current_page-3) if (current_page-3) > 0 else 0:current_page-1]
        if len(left) > 0 and left[0] > 2:
            left_has_more = True
        if len(left) > 0 and left[0] > 1:
            first = True

        context = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
        }

        return context



def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.increase_views()
    # to create an instance of markdown
    md = markdown.Markdown(extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                        TocExtension(slugify = slugify),
                                     ])
    article.body = md.convert(article.body)
    form = CommentForm()
    comment_list = article.comments_set.all()

    context = {'article':article,
               'form':form,
               'comment_list':comment_list,
               'toc': md.toc}
    return render(request, 'blog/detail.html', context=context)

def archives(request, year, month):
    article_list = Article.objects.filter(create_time__year = year,
                                          create_time__month = month).order_by('-create_time')
    return render(request, 'blog/index.html', context={'article_list':article_list})

def categories(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    article_list = Article.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog/index.html', context={'article_list':article_list})

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = 'Please input keyword'
        return render(request, 'blog/index.xml', {'error_msg':error_msg})

    article_list = Article.objects.filter(title__icontains=q)
    return render(request, 'blog/index.html', context={'error_msg': error_msg,
                                               'article_list':article_list})


