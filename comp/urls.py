from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
       url(r'^index/$', views.index,name='index'),
       #url(r'^search/',views.search, name = 'search'),
       url(r'^scrapy/search/',views.scrapy,name = 'scrapy'),
       #url(r'^scrapy/search/',views.scsearch, name = 'scsearch'),
       url(r'^scrapy/details/(?P<comp>.*)/',views.scdetail,name = 'scdetail'),
]