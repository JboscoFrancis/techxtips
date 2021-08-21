from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils import timezone
from random import randint
from PIL import Image

# Create your models here.
class Post(models.Model):
    CATEGORY = (
        ('Computer', 'Computer'),
        ('django', 'django'),
        ('html', 'html'),
        ('css', 'css'),
        ('js', 'js'),
        ('python', 'python'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, null=True)
    descriptions = models. TextField(max_length=400, null=True)
    body = RichTextField(max_length=64600, null=True)
    likes = models.ManyToManyField(User, related_name = 'likes', blank=True)
    category = models.CharField(max_length=255,choices=CATEGORY, null=True)
    # tags = TaggableManager()
    slug = models.SlugField(max_length=250, null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='thumbnail')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def imageurl(self):
        try:
            url = self.thumbnail.url
        except:
            url = ""
        return url

    @property
    def likes_count(self):
        count = self.likes.count()
        return count

    def save(self, *args, **kwargs):
        slug = slugify(self.title)
        qr = Post.objects.filter(slug=slug)
        if qr.count() > 1:
            self.slug = slug + str(randint(0, 44))
        else:
            self.slug = slug

        #modify post
        print(self.date_created)
        print(timezone.now())
        if self.date_created != None:
            self.date_modified = timezone.now()

        super().save(*args, **kwargs)
        img = Image.open(self.thumbnail.path)
        if img.width > 600 or img.height > 350:
            output_size = (600, 350)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)
        
    





class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=1200, null=True)
    date_comment = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment= models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField(max_length=1200, null=True)
    date_reply = models.DateTimeField(auto_now_add=True)

    class Meta:
        # verbose_name = 'company'
        ordering = ['-date_reply']

class Subscriber(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(unique=True, max_length=255, null=True)

    def __str__(self):
        return self.name

class Rate(models.Model):
    name = models.CharField(max_length=255, null=True)
    star = models.IntegerField()

class News(models.Model):
    title = models.TextField(max_length=255, null=True)
    descriptions = models.TextField(max_length=360, null=True)
    link = models.CharField(max_length=1200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.title

    class Meta:
        # verbose_name = 'company'
        verbose_name_plural = 'News'

class Tips(models.Model):
    title = models.CharField(max_length=255, null=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='tips')
    descriptions = RichTextField(max_length=2400, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.title

    class Meta:
        # verbose_name = 'company'
        verbose_name_plural = 'Tips'

    @property
    def imageurl(self):
        try:
            url = self.thumbnail.url
        except:
            url = ""
        return url
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.thumbnail.path)
        if img.width > 300 or img.height > 250:
            output_size = (300, 250)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)
