from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.six import python_2_unicode_compatible
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

class Tag(models.Model):
    name = models.CharField(max_length=100)

@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200,blank=True)

    category = models.ForeignKey(Category)
    tags  = models.ManyToManyField(Tag,blank=True)

    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

        # 自定义 get_absolute_url 方法
        # 记得从 django.urls 中导入 reverse 函数

    def get_absolute_url(self):
        return reverse('myblog:detail',args=[self.pk])

    class Meta:
        ordering = ['-created_time']