from rest_framework import generics,status,views,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import RegisterSerializer,LoginSerializer,LogoutSerializer,UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import *
# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        try:
            serializer = self.serializer_class(data=user)
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            user_data = serializer.data
            return Response(user_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message':'Unfortunately, something went wrong. Please try again later.','error:':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except AuthenticationFailed as auth_failed:
            return Response({'message': str(auth_failed)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(
                {'message': 'Unfortunately, something went wrong. Please try again later.', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'message':'logout sucessful'},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message':'Unfortunately, something went wrong. Please try again later.','error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
class CurrentUserView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'Unfortunately, something went wrong. Please try again later.','error:':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        try:
            user=request.user
            serializer=UserSerializer(user,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'Unfortunately, something went wrong. Please try again later.','error:':str(e)},status=status.HTTP_400_BAD_REQUEST)