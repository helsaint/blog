from django.shortcuts import render
from .models import QuillPost
import re
from json import dumps
from html.parser import HTMLParser

#Get all blog entries
def BlogHome(request):
    data = QuillPost.objects.all()
    lst_return = []
    removeTags = re.compile('<.*?>')
    for d in data:
        dictTemp = {}
        dictTemp['ID'] = d.id
        strTempH1 = re.search(r'(<h1.*?>.*?<\/h1>)',str(d.content.html)).group(0)
        dictTemp['Title'] = strTempH1[4:len(strTempH1)-5]
        strTemp = str(d.content.html)[:250]
        strTemp = re.sub(removeTags, '', strTemp)
        dictTemp['First100'] = strTemp
        lst_return.append(dictTemp)

    return render(request, 'blog.html', {'blog_data': lst_return})
    #return render(request, 'blog.html', {'blog_data': data})

#Get blog entry by primary key value(id). It's returned to the blog_detail.html details page
def BlogDetail(request, id):
    data = QuillPost.objects.get(id=id)
    return render(request,'blog_detail.html', {'blog_data': data})
# Create your views here.
