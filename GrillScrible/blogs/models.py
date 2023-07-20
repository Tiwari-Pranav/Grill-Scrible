from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.
class Tag(models.Model):
    '''Model to maintain tags'''
    name=models.CharField(max_length=20)
    description=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural='Tags'
        verbose_name='Tag'

class IpModel(models.Model):
    '''Model to maintain addresses information'''
    ip=models.CharField(max_length=100)   
    
    def __str__(self):
        return self.ip
    
class Blog(models.Model):
    '''Model to maintain blog information'''
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name="authors_blogs")
    title=models.CharField(max_length=50)
    #short summary for cover pages and tile view
    intro=models.CharField(max_length=200)
    # full content of blogs
    description=models.TextField(max_length=None)
    thumbnail=models.ImageField(upload_to='blog',default='blog/blog_default.jpg')
    # associated tags
    tags = models.ManyToManyField(Tag, blank=True, related_name='related_blogs')
    date_published=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)
    # Record Ip addresses which liked this blog (max one like per Ip address)
    likes_ip=models.ManyToManyField(IpModel,related_name="blog_like_ip",blank=True)
    # Like count is recorded seprate as Ip address need to be cleared after fixed time
    likes_count=models.IntegerField(default=0)
    # Give admin un-publish access (for inappropriate content)
    published=models.BooleanField(default=True)
    
    def __str__(self):
        return f'{str(self.author)} | {str(self.title)}'
    
    @property
    def blog_name(self):
        return f'{str(self.id)} . {self.title}'
    
    class Meta:
        verbose_name_plural='Blogs'
        verbose_name='Blog'
    
class Comment(models.Model):
    # Since anonymous user can comment 
    comment_user=models.CharField(max_length=20)
    remark=models.CharField(max_length=200,null=True)
    created=models.DateTimeField(auto_now_add=True)
    # To take down inappopriate comments
    active=models.BooleanField(default=True)
    # Refernce to the associated blog
    related_blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="comments")
    
    def __str__(self):
        return f'{str(self.comment_user)} - {self.related_blog.title}'        
    
    class Meta:
        verbose_name_plural='Comments'
        verbose_name='Comment'               
        
