from rest_framework import serializers
from blogs.models import Blog, Comment, Tag

class CommentSerializer(serializers.ModelSerializer):
    '''Serializer for comment message'''
    class Meta:
        model=Comment
        fields='__all__'
        # user should not be allowed to update this field
        read_only_fields=['active','related_blog']

class BlogSerializer(serializers.ModelSerializer):
    '''Serializer for Blog post'''
    
    # comments of that individual blog
    comments=CommentSerializer(many=True,read_only=True)
    # using writer to avoid conflict with author value comming from view
    writer = serializers.CharField(source='author.first_name',read_only=True)
    # tags of that individual blog
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name'
    )
    class Meta:
        model=Blog
        # user can't update these
        read_only_fields = ['id','date_updated','date_published','likes_count','author','published']
        # user doesn't need to know
        exclude=['likes_ip',]
        
class TagSerializer(serializers.ModelSerializer):
    '''Serializer for Tag element'''
    # Blog related to individual tag   element
    related_blogs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='blog_name'
    )
    class Meta:
        model=Tag
        fields='__all__'

