from rest_framework import generics,status,views,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import *
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import RegisterSerializer,LoginSerializer,LogoutSerializer,UserSerializer
from .models import Session
from django.contrib.auth import get_user_model
# Create your views here.
from .models import Session
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
            outstanding_token = OutstandingToken.objects.get(token=serializer.data['tokens']['refresh'])
            # Create a new Session instance to store the OutstandingToken and user information
            user=get_user_model().objects.get(username=serializer.data['username'])
            Session.objects.create(out_token=outstanding_token, client=user)
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
            try:
                session = Session.objects.get(out_token__token=serializer.data['refresh'])
                session.delete()
                return Response({'message':'Logout successful'},status=status.HTTP_204_NO_CONTENT)
            except Session.DoesNotExist:
                return Response({'error': 'Invalid refresh token'}, status=400)
        except Exception as e:
            return Response({'message':'Unfortunately, something went wrong. Please try again later.','error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class CustomTokenRefreshAPIView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')

            # Decode the refresh token
            refresh_token = RefreshToken(refresh_token)

            session = Session.objects.get(out_token__token=refresh_token)
        except Session.DoesNotExist:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Proceed with token refresh if the session exists
        return super().post(request, *args, **kwargs)

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