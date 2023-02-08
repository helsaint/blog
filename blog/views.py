from django.shortcuts import render, redirect
from .models import QuillPost
import re
from json import dumps
from .forms import CustomForm

#Get all blog entries and setup contact form
def BlogHome(request):
    #List of dictionaries collecting blog entries
    lst_return = BlogLstDict(request)
    #Checks if form is submitted
    bool_submit = FormSubmit(request)
    if(bool_submit):
        return redirect("blog")
    else:
        form = CustomForm()
    return render(request, 'blog.html', {'blog_data': lst_return, 'form': form})
    
#Populate blog_data dictionary for blog entries
def BlogLstDict(request):
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
    return lst_return

def FormSubmit(request):
    if request.method == "POST":
        form = CustomForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.save()
            return True
    return False

#Get blog entry by primary key value(id). It's returned to the blog_detail.html details page
def BlogDetail(request, id):
    data = QuillPost.objects.get(id=id)
    return render(request,'blog_detail.html', {'blog_data': data})

