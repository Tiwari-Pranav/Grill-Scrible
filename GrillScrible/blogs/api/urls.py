from django.urls import path
from blogs.api.views import *


urlpatterns = [
    path('list/',BlogListAView.as_view(), name='blog_list'),
    path('<int:pk>/',BlogDetailAView.as_view(), name='blog_description'),
    
    path('mylist/',UserBlogListAView.as_view(), name='my_blog_list'),
    
    path('tags/',TagListAView.as_view(), name='tags'),
    path('tags/<int:pk>/',TagDetailAView.as_view(), name='tags-detail'),
    
    
    path('<int:pk>/comments/',CommentListAView.as_view(), name='comment_list'),
    path('comments/<int:pk>/',CommentDetailAView.as_view(), name='comment_detail'),
    
    path('<int:pk>/like/',blog_like, name='like_feature'),
]