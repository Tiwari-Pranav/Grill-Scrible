from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import *
from blogs.serializers import *
from blogs.models import Blog, Comment, Tag, IpModel
from common.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from common.pagination import ListPageNumberPagination
# In requirment of the project, class based views are instructed

class TagListAView(APIView):
    #Only admin can create tags
    permission_classes=[IsAdminOrReadOnly] 
    def get(self,request):
        try:
            tag=Tag.objects.all()
            serializer=TagSerializer(tag,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Tag.DoesNotExist:
            return Response({'message':'Does not exist'},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        try:
            serializers=TagSerializer(data=request.data)
            if not serializers.is_valid():
                return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message':'Request failed: Please come back later and try again.','error':str(e)},status=status.HTTP_400_BAD_REQUEST)
class TagDetailAView(APIView):
    #Only admin can edit or delete tags 
    permission_classes=[IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            tag=Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({'message':'Does not exist'},status=status.HTTP_404_NOT_FOUND)
        serializer=TagSerializer(tag,context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        try:
            tag=Tag.objects.get(pk=pk)
            serializer=TagSerializer(tag,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'Request failed: Please come back later and try again.','error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        try:
            tag=Tag.objects.get(pk=pk)
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message':'Request failed: Please come back later and try again.','error':str(e)},status=status.HTTP_400_BAD_REQUEST)

#Concrete View Classes can be used to create Tag views easily
class BlogListAView(generics.ListCreateAPIView):
    serializer_class=BlogSerializer
    #Only authenticated users can create a new blog
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class= ListPageNumberPagination
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def get_queryset(self):
        '''Adding serach functionality'''
        queryset = Blog.objects.filter(published=True) #filter inappropriate data
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(author__first_name__icontains=search) | queryset.filter(author__username__icontains=search) | queryset.filter(author__last_name__icontains=search) | queryset.filter(tags__name__icontains=search)| queryset.filter(title__icontains=search)| queryset.filter(intro__icontains=search)| queryset.filter(description__icontains=search)
         #latest blogs should come up first
        queryset=queryset.order_by('-date_updated','-date_published')
        return queryset
 
   
        
class BlogDetailAView(generics.RetrieveUpdateDestroyAPIView):
    #User must be author,or staff to edit
    permission_classes=[IsAuthorOrReadOnly]
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
            
class UserBlogListAView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class=BlogSerializer
    def get_queryset(self):
        """
        This view should return a list of all the blogs
        for the currently authenticated user.
        """
        user = self.request.user
        return Blog.objects.filter(author=user)    


class CommentListAView(generics.ListAPIView,generics.CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=CommentSerializer
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Comment.objects.filter(related_blog=pk,active=True) #filter inappropriate comments
    
    def perform_create(self, serializer):
        pk=self.kwargs['pk']
        blog_item=Blog.objects.get(pk=pk)
        serializer.save(related_blog=blog_item)
    
class CommentDetailAView(generics.RetrieveUpdateDestroyAPIView): 
    #Only admin can delete or unactive comments
    permission_classes=[IsAdminOrReadOnly]
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer

def get_client_ip(request):
    return (
        x_forwarded_for.split(',')[0]
        if (x_forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR'))
        else request.META.get('REMOTE_ADDR')
    )    

from rest_framework.decorators import api_view
@api_view(http_method_names=['POST'])
def blog_like(request,pk):
    try:
        blog=Blog.objects.get(pk=pk)
        ip=get_client_ip(request)
        #If IP is not in the IpModel then allow to like
        if not IpModel.objects.filter(ip=ip).exists():
            ip_model=IpModel(ip=ip)
            ip_model.save()
            blog.likes_ip.add(ip_model)
            blog.likes_count=blog.likes_count+1
            blog.save()
            return Response({"like":True},status.HTTP_200_OK)
        #If IP is in the IpModel BUT not in blog.likes_ip then allow to like as it must be stored when it liked some other blog
        elif not blog.likes_ip.filter(ip=IpModel.objects.get(ip=ip).ip).exists():
            blog.likes_count=blog.likes_count+1
            blog.likes_ip.add(IpModel.objects.get(ip=ip))
            print(blog.likes_count)
            blog.save()
            return Response({"like":True},status.HTTP_200_OK)
            
        return Response({"message":"Already liked"},status=status.HTTP_429_TOO_MANY_REQUESTS)
    except Exception as e:
        return Response({"message":"Somthing went wrong",'error':str(e)},status=status.HTTP_400_BAD_REQUEST)