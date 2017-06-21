from django.db import models
from django.contrib.auth.models import User

# to fetch the absolute url
from django.urls import reverse

import markdown
from django.utils.html import strip_tags


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length = 100)
    body = models.TextField()

    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    summary = models.CharField(max_length = 200, blank = True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank = True)

    author = models.ForeignKey(User)

    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

    def increase_views(self):
        self.view_count += 1
        self.save(update_fields = ['view_count'])

    # auto create summary
    def save(self, *args, **kwargs):
        if not self.summary:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.summary = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    class Meta:
        # do not need to order everytime
        ordering = ['-create_time']




