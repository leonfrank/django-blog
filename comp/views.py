import markdown
from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse
from .scrapy import *
from .models import CompResult
from django.db.models import Sum,Q
from datetime import timedelta,datetime

def index(request):
    return render(request, 'comp/index.html')
# Create your views here.
def scrapy(request):
    q = request.GET.get('q')
    keywords = request.GET.get('keywords')
    #print(q,keywords)
    if not q:
        error_msg = '请输入公司名'
        return render(request,'comp/error.html',{'error_msg':error_msg})
    elif not keywords:
        error_msg = '请输入关键字'
        return render(request, 'comp/error.html', {'error_msg': error_msg})
    searchOptions = default_searchOptions()
    comps = q.strip().split()
    #CompResult.objects.all().delete()
    for comp in comps:
        newsData = get_list(comp,keywords,searchOptions)
        for record in newsData:

            compresult = CompResult(title = record['title'],company = comp,created_time = record['scrapy_time'],title_score = record['title_score'],wx_link = record['wx_link'])
            compresult.save()
    starttime,endtime = datetime.now()-timedelta(days=1),datetime.now()
    comp_list = CompResult.objects.all().filter(created_time__range=[starttime,endtime]).values('company').annotate(title_score = Sum('title_score')).order_by()

    #print(type(comp_list))
    return render(request,'comp/scrapy.html',{'comp_list':comp_list})
def scdetail(request,comp):
    starttime, endtime = datetime.now() - timedelta(days=1), datetime.now()
    details = CompResult.objects.filter(Q(company = comp),created_time__range = [starttime,endtime] )
    #print(type(details))
    return render(request,'comp/detail.html',{'comp':comp,'details':details})

