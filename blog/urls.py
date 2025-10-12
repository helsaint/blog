from django.urls import path
from . import views

urlpatterns = [
    path("blog/<int:id>/", views.BlogDetail, name="blog_detail"),
    path("search/", views.search_results_view, name="search_results"),
    path("", views.BlogHome, name="blog"),
]
