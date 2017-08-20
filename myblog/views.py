import markdown
from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse
from myblog import models
from .models import Post,Category


# Create your views here.

def index(request):
    post_list =  Post.objects.all().order_by('-created_time')
    return render(request, 'myblog/index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,extensions=['markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',])
    return render(request, 'myblog/detail.html', context={'post': post})

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'myblog/index.html', context={'post_list': post_list})

def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'myblog/index.html', context={'post_list': post_list})

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request,'myblog/error.html',{'error_msg':error_msg})

    post_list = Post.objects.filter(title__icontains=q)
    return render(request,'myblog/results.html',{'error_msg':error_msg,'post_list':post_list})