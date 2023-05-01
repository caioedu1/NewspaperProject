from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
# Create your models here

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])
    
class Comment(models.Model): # new
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length= 1000)
    author = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE,
    related_name='comments'
    )
    def __str__(self):
        return self.comment
    def get_absolute_url(self):
        return reverse('article_list')
    
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
