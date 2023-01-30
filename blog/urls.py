from django.urls import path
from . import views

urlpatterns = [
    path('blog/<int:id>/', views.BlogDetail, name='blog_detail'),
    path('', views.BlogHome, name='blog'),
]