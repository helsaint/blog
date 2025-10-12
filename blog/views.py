from django.shortcuts import render, redirect
from .models import QuillPost
import re
from json import dumps
from .forms import CustomForm
from urllib.request import urlopen


# Get all blog entries and setup contact form
def BlogHome(request):
    # List of dictionaries collecting blog entries
    lst_return = BlogLstDict(request)
    # Checks if form is submitted
    bool_submit = FormSubmit(request)
    if bool_submit:
        return redirect("blog")
    else:
        form = CustomForm()
    return render(request, "blog.html", {"blog_data": lst_return, "form": form})


# Populate blog_data dictionary for blog entries
def BlogLstDict(request):
    data = QuillPost.objects.all()
    lst_return = []
    removeTags = re.compile("<.*?>")
    for d in data:
        dictTemp = {}
        dictTemp["ID"] = d.id
        strTempH1 = re.search(r"(<h1.*?>.*?<\/h1>)", str(d.content.html)).group(0)
        dictTemp["Title"] = strTempH1[4 : len(strTempH1) - 5]
        url_add_on = dictTemp["Title"]
        url_add_on = url_add_on.replace(" ", "+")
        url_image = LexicaArtScrape(url_add_on)
        dictTemp["Image"] = url_image
        strTemp = str(d.content.html)[:250]
        strTemp = re.sub(removeTags, "", strTemp)
        dictTemp["First100"] = strTemp
        lst_return.append(dictTemp)

    return list(reversed(lst_return))


# Get AI generated image from lexica using the 100 word description of the article
def LexicaArtScrape(search_term):
    url_base = "https://lexica.art/?q="
    page = ""
    try:
        page = urlopen(url_base + search_term, timeout=2)
    except:
        print(page)
        return (
            "https://upload.wikimedia.org/wikipedia/commons/c/c3/JPEG_format_logo.svg"
        )
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    start_text = "images="
    end_text = "&amp;"
    pattern = re.compile(f"(?<={re.escape(start_text)})(.*?)(?={re.escape(end_text)})")
    url_matches = pattern.findall(html)

    for i in url_matches:
        pattern = re.compile(r"^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$")
        if bool(pattern.match(i)):
            return i

    return "https://upload.wikimedia.org/wikipedia/commons/c/c3/JPEG_format_logo.svg"


# Non Functional
def FormSubmit(request):
    if request.method == "POST":
        form = CustomForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.save()
            return True
    return False


# Get blog entry by primary key value(id). It's returned to the blog_detail.html details page
def BlogDetail(request, id):
    data = QuillPost.objects.get(id=id)
    return render(request, "blog_detail.html", {"blog_data": data})

# Search function using Google Custom Search Engine
def search_results_view(request):
    return render(request, "search.html",{})   
