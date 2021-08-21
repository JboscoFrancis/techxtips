from django.contrib import admin
from . models import Post, Comment, Reply, News, Rate, Subscriber, Tips
from django import forms
from ckeditor.widgets import CKEditorWidget
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(News)
admin.site.register(Rate)
admin.site.register(Subscriber)
admin.site.register(Tips)