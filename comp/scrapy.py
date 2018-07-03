import requests
import sys
import urllib.request
import re
import os
from  bs4 import BeautifulSoup
from urllib.parse import urlencode
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from blog.settings import BASE_DIR
from django.utils import timezone
import datetime
from collections import OrderedDict

def scoring(line,keywords):
    score = 0
    for kwd in keywords:
        if line.find(kwd)!=-1:
            score = score - 10
    return score
def get_wx_body(wx_link):
    wx_headers = {
        "Host": "mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        # "Referer":"http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4&tsn=1&ft=&et=&interation=&wxid=&usip="
    }
    req = urllib.request.Request(wx_link, headers=wx_headers)
    response = urllib.request.urlopen(req)
    h = response.read()
    soup = BeautifulSoup(h,'html.parser')
    paras = soup.find_all('p')
    body = [p.get_text() for p in paras]
    return ''.join(body)
def get_list(comp,keywords,searchOptions):
    newsData = []
    start_url = "http://weixin.sogou.com/weixin?"
    keywords = keywords.strip().split()

    def extract_content(div,keywords):
        title = div.find('a').get_text()
        wx_link = div.find('a').get('href')
        #body = get_wx_body(wx_link)
        title_score = scoring(title,keywords)
        #body_score = scoring(body,keywords)
        script = div.find('script')
        timestamp = re.search('\d+', script.get_text()).group(0)
        scrapy_time= datetime.datetime.fromtimestamp(
            int(timestamp))
        cont = {'title':title,'scrapy_time':scrapy_time,'title_score':title_score,'wx_link':wx_link}
        return  cont
    query = comp
    d = {'type': 2 ,'ie':'utf8','query':query,'page':1}
    d.update(searchOptions)

    for i in range(1,11):
        d['page'] = i
        pname  = urlencode(d)
        href = start_url + pname
        #print(href)
        hdr = {"Host":"weixin.sogou.com","Referer":href,"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
        req = urllib.request.Request(href,headers = hdr)
        response = urllib.request.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html,'html.parser')
        '''div = soup.find('div',{"class":"mun"})
        line = div.contents[0].replace(',','')
        num = int(re.findall(r'[0-9]+',line)[0])
        newsData[kwd] = num'''
        divs = soup.find_all('div',{'class':'txt-box'})

        for div in divs:
            newsData.append(extract_content(div,keywords))
    '''
    x_label = range(len(keywords))
    y_data = newsData.values()
    font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\msyhl.ttc", size=14)  # C:\WINDOWS\Fonts
    plt.bar(x_label,y_data,align ='center',alpha = 0.5)
    plt.xticks(x_label,keywords,fontproperties = font)
    plt.ylabel(u"搜索结果条数",fontproperties=font)
    plt.title((u"%s公司微信关键词搜索统计" %comp),fontproperties = font)
    TT = str(int(time.time()))
    plt.savefig('static/comp/img/'+comp+'-'+TT+'.png')
    '''
    return newsData

def default_searchOptions():
    searchOptions = {}
    # tsn = 1 & ft = & et = & interation = & wxid = & usip =
    searchOptions['tsn'] = 1
    searchOptions['ft'] = ''
    searchOptions['et'] = ''
    searchOptions['interation'] = ''
    searchOptions['wxid'] = ''
    searchOptions['usip'] = ''
    return searchOptions

def main():
    comp = "阿里巴巴"
    keywords = "违约 诉讼 法院 风险"
    searchOptions = default_searchOptions()
    newsData = get_list(comp,keywords,searchOptions)
    print(newsData[0]['title'],newsData[0]['body'])

if __name__=='__main__':
    main()