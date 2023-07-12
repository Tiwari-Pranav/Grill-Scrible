from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from blogs.models import *
from blogs.api.serializers import *

# Create your tests here.
class TagTestCase(APITestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username='testuser',password='Password@123')
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

        #manually create a tag
        self.tag=Tag.objects.create(name='testtag',description='test tag description')
        
    def test_tag_create(self):
        data={
            "name":"Test Tag",
            "description":"Test Tag Description"
        }
        response = self.client.post(reverse('tags'), data)
        # Since the a tag can be created only by admin so a non-admin will recieve 403 Forbidden response.
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_tag_list(self):
        # Testing to recieve a list of tags
        response=self.client.get(reverse('tags'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_tag_detail(self):
        # Testing to revieve a details of an individual tag
        response=self.client.get(reverse('tags-detail',args=[self.tag.id]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['name'],self.tag.name)
        self.assertEqual(response.data['description'],self.tag.description)
        
class BlogListTestCase(APITestCase):
    
    def setUp(self):
        self.user=get_user_model().objects.create_user(username='testuser',password='Password@123')
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        #manually create a tag
        self.tag=Tag.objects.create(name='testtag',description='test tag description')
        
        
    def test_blog(self):
        data={
            "title":"Test Blog",
            "intro":"Test Blog Introduction",
            "description":"Test Blog Description",
            "tags":[self.tag]
        }
        # Testing to add a blog 
        response=self.client.post(reverse('blog_list'),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tags'],[self.tag.name])
        blog_id=response.data['id']

        # Test to get a blogs list
        response=self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testing the detail view for the blog added
        response=self.client.get(reverse('blog_description', args=[blog_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['author'],self.user.id)
        
        
        #Testing to update a blog 
        data={
            "title":"New Test Blog",
            "intro":"New Test Blog Introduction",
            "description":"New Test Blog Description",
            "tags":[self.tag]
        }
        response=self.client.put(reverse('blog_description', args=[blog_id]),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checking the response data against the data sent to certify the update
        self.assertEqual(response.data['author'],self.user.id)
        self.assertEqual(response.data['title'],data['title'])
        self.assertEqual(response.data['intro'],data['intro'])
        self.assertEqual(response.data['description'],data['description'])
        
        #Testing to delete the blog
        response=self.client.delete(reverse('blog_description', args=[blog_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
class CommentTestCase(APITestCase):
    
        def setUp(self):
            self.user= get_user_model().objects.create_user(username='testuser',password='Passwprd@123')
            self.blog=Blog.objects.create(author=self.user,title='testblog',intro='Test blog intro', description='Test blog description')
            self.comment= Comment.objects.create(related_blog=self.blog,comment_user='UserTesting',remark='Test blog description')
            
        def test_create_comment(self):
            # Testing to add a comment to a blog
            data={
                "comment_user":"Test user",
                "remark":"Test Comment"
            }
            response= self.client.post(reverse('comment_list',args=[self.blog.id]),data)
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            
        def test_create_list(self):
            # Testing to list all comments to a blog
            response= self.client.get(reverse('comment_list',args=[self.blog.id]))
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            
        def test_comment_detail(self):
            # Testing to list detail of a individual comment
            response=self.client.get(reverse('comment_detail',args=[self.comment.id]))
            self.assertEqual(response.status_code,status.HTTP_200_OK)
    
        def test_comment_delete(self):
            # Testing to delete a comment
            response=self.client.delete(reverse('comment_detail',args=[self.comment.id]))
            # No one except admin can delete any comments
            self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

class LikeTestCase(APITestCase):
    
    def setUp(self):
        self.user= get_user_model().objects.create_user(username='testuser',password='Passwprd@123')
        self.blog=Blog.objects.create(author=self.user,title='testblog',intro='Test blog intro', description='Test blog description')
        
    def test_like_feature(self):
        # Testing to check the like feature
        response=self.client.post(reverse('like_feature',args=[self.blog.id]))    
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        #one user cannot like the blog twice
        response=self.client.post(reverse('like_feature',args=[self.blog.id]))    
        self.assertEqual(response.status_code,status.HTTP_429_TOO_MANY_REQUESTS)