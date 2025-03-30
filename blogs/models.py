from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse



# Create your models here.
class Post(models.Model):
    author  = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    title = models.CharField(null=False, blank=False, max_length = 50)
    text = models.TextField(null=False, blank = False)
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True, null = True)
    edited = models.BooleanField(default=False)
    likes = models.IntegerField(default = 0)
    dislikes = models.IntegerField(default = 0)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='thumbnail_pics')
    TOPIC_CHOICE = (
        ('World','World'),
        ('Technology','Technology'),
        ('Design','Design'),
        ('Culture','Culture'),
        ('Business','Business'),
        ('Politics','Politics'),
        ('Opinion','Opinion'),
        ('Science','Science'),
        ('Health','Health'),
        ('Style','Style'),
        ('Travel','Travel'),
        ('Others','Others'),
    )
    topic = models.CharField(max_length = 11,choices = TOPIC_CHOICE, default="Others", blank=False, null=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        if self.published_date == None:
            return reverse('blogs:draft-list', kwargs={'username':str(self.author)})
        else:
            return reverse('blogs:blogs-index')

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    post = models.ForeignKey('blogs.Post', related_name='comments', on_delete = models.CASCADE)
    comment = models.TextField(null = False, blank = False)
    created_date = models.DateTimeField(default = timezone.now)
    likes = models.IntegerField(default = 0)
    dislikes = models.IntegerField(default = 0)

    def get_absolute_url(self):
        return reverse('blogs:post-details', kwargs={'pk':self.post.pk})

    def __str__(self):
        return self.comment

class PostPreference(models.Model):
    user = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    post = models.ForeignKey(Post,on_delete = models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.post.title


class CommentPreference(models.Model):
    user = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete = models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.comment

class PostReport(models.Model):
    user = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    FEEDBACK_CHOICE = (
        ('Nudity','Nudity'),
        ('Violence','Violence'),
        ('Harassment','Harassment'),
        ('Sucide or Self-Injury','Sucide or Self-Injury'),
        ('False News','False News'),
        ('Spam','Spam'),
        ('Unauthorized Sales','Unauthorized Sales'),
        ('Hate Speech','Hate Speech'),
        ('Terrosim','Terrosim'),
    )
    feedback = models.CharField(max_length = 30,choices = FEEDBACK_CHOICE,blank=False,null=False)
    feedback_text = models.TextField(max_length = 60,blank=True,null=True)
    date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.feedback

    def get_absolute_url(self):
        return reverse('blogs:post-details', kwargs={'pk':self.post.pk})
