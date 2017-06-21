from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Article

from .models import Comments
from .forms import CommentForm

# Create your views here.
def article_comment(request, pk):
    article = get_object_or_404(Article, pk = pk)

    # submit forms
    if request.method == 'POST':
        # all information in the POST section
        form = CommentForm(request.POST)

        if form.is_valid():
            # create a instance of form, but do not submit POST data
            commit = form.save(commit=False)
            # fulfil the article section
            commit.article = article

            commit.save()

            # show the article page.
            return redirect(article)
        else:
            # re-render this page
            comment_list = post.comments_set.all()
            context = {'article': article,
                       'form':form,
                       'comment_list':comment_list
                       }
            return render(request, 'blog/detail.html', context = context)
    # show the article page
    return redirect(article)




