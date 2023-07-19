from rest_framework import serializers
from blogs.models import Blog, Comment, Tag

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'
        read_only_fields=['active','related_blog']

class BlogSerializer(serializers.ModelSerializer):
    comments=CommentSerializer(many=True,read_only=True)
    #using writer to avoid conflict with author value comming from view
    writer = serializers.CharField(source='author.first_name',read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name'
    )
    class Meta:
        model=Blog
        read_only_fields = ['id','date_updated','date_published','likes_count','author','published']
        exclude=['likes_ip',]
        
class TagSerializer(serializers.ModelSerializer):
    related_blogs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='blog_name'
    )
    class Meta:
        model=Tag
        fields='__all__'

