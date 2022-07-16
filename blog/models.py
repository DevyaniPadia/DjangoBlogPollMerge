from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
# from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.text import slugify   
import datetime



class User(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    mobile_no = models.IntegerField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_img',null=True)

    def __str__(self):
        return self.username

    
class Category(models.Model):
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):  
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('add_category', kwargs={'pk': self.pk})


class Tag(models.Model):
    tname = models.CharField(max_length=200)
    text=models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.tname
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField('date published')
    slug = models.SlugField(null=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # tags = TaggableManager()
    tag = models.ManyToManyField(Tag)
    thumbnailimage = models.ImageField(upload_to='thumbnail')
    featureimage = models.ImageField(upload_to='featureimage')


    class Meta:
        verbose_name="Post Created"

    # @admin.display(
    #     boolean=True,
    #     ordering='published_date',
    #     description='Published recently?',
    # )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_date <= now

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    

    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replies')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


