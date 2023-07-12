from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.
class Tag(models.Model):
    name=models.CharField(max_length=20)
    description=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural='Tags'
        verbose_name='Tag'

class IpModel(models.Model):
    ip=models.CharField(max_length=100)   
    
    def __str__(self):
        return self.ip
    
class Blog(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name="authors_blogs")
    title=models.CharField(max_length=50)
    intro=models.CharField(max_length=200)
    description=models.TextField(max_length=None)
    thumbnail=models.ImageField(upload_to='blog',default='blog/blog_default.jpg')
    tags = models.ManyToManyField(Tag, blank=True, related_name='related_blogs')
    date_published=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)
    likes_ip=models.ManyToManyField(IpModel,related_name="blog_like_ip",blank=True)
    likes_count=models.IntegerField(default=0)
    published=models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.author)+" | "+str(self.title)
    
    @property
    def blog_name(self):
        return str(self.id)+". "+self.title
    
    class Meta:
        verbose_name_plural='Blogs'
        verbose_name='Blog'
    
class Comment(models.Model):
    comment_user=models.CharField(max_length=20)
    remark=models.CharField(max_length=200,null=True)
    created=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    related_blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="comments")
    
    def __str__(self):
        return str(self.comment_user)+ "-"+ self.related_blog.title        
    
    class Meta:
        verbose_name_plural='Comments'
        verbose_name='Comment'               