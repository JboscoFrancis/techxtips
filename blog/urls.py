from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.blog, name='blog'),
    path('post/<slug:slug>', views.post, name='post'),
    path('create_post', views.create_post, name='create_post'),
    path('update_post/<slug:slug>', views.update_post, name='update'),
    path('likepost', views.likepost, name='likepost'),
    path('userlogin', views.userlogin, name='userlogin'),
    path('userlogout', views.userlogout, name='userlogout'),
    path('register', views.register, name='register'),
    path('service', views.service, name='service'),
    path('contact', views.contact, name='contact'),
    path('user/account', views.account, name='account'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('reply_comment', views.reply, name='reply'),
    path('tips', views.tips, name='tips'),
    path('tips/<str:title>/<int:pk>', views.tips_detail, name='tips_detail'),
]