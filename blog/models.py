from django.db import models
from django_quill.fields import QuillField

class QuillPost(models.Model):
    content = QuillField()
# Create your models here.

# Model for User feed back
class UserResponseModel(models.Model):
    name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=False)
    subject = models.CharField(max_length=100, blank=False)
    message = models.TextField(max_length=1000, blank=False)
