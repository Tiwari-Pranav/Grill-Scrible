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
from .models import Session
# Create your views here.

class RegisterView(generics.GenericAPIView):
    '''View for new users to register'''
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        try:
            serializer = self.serializer_class(data=user)
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            #save the user
            serializer.save()
            user_data = serializer.data
            return Response(user_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message':'Unfortunately, something went wrong. Please try again later.','error:':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class LoginAPIView(generics.GenericAPIView):
    '''View for user login'''
    serializer_class = LoginSerializer
    def post(self,request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                #if data entered is not valid
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            #retrieve the outstanding refresh token
            outstanding_token = OutstandingToken.objects.get(token=serializer.data['tokens']['refresh'])
            
            # Create a new Session instance to store the OutstandingToken and user information
            user=get_user_model().objects.get(username=serializer.data['username'])
            Session.objects.create(out_token=outstanding_token, client=user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        # Incase authentication fails
        except AuthenticationFailed as auth_failed:
            return Response({'message': str(auth_failed)}, status=status.HTTP_401_UNAUTHORIZED)
        # If any other exception occurs during excecution 
        except Exception as e:
            return Response(
                {'message': 'Unfortunately, something went wrong. Please try again later.', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class LogoutAPIView(generics.GenericAPIView):
    '''View for user logout'''
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            try:
                # If the data is valid then check if a session exist for corresponding refresh token. If so then delete the session
                session = Session.objects.get(out_token__token=serializer.data['refresh'])
                session.delete()
                return Response({'message':'Logout successful'},status=status.HTTP_204_NO_CONTENT)
            # If session does not exist then return error message
            except Session.DoesNotExist:
                return Response({'error': 'Invalid refresh token'}, status=400)
        # For unexpected errors
        except Exception as e:
            return Response({'message':'Unfortunately, something went wrong. Please try again later.','error':str(e)},status=status.HTTP_400_BAD_REQUEST)

class CustomTokenRefreshAPIView(TokenRefreshView):
    '''We do not want to refresh the tokens of user who are logged out so we define custom refresh view'''
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')

            # Decode the refresh token
            refresh_token = RefreshToken(refresh_token)
            # Check if a session corresponding to the refresh token exist   
            session = Session.objects.get(out_token__token=refresh_token)
        
        # If session does not exist then user must have logged out but refresh token may still exist
        except Session.DoesNotExist:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Proceed with token refresh if the session exists
        return super().post(request, *args, **kwargs)

class CurrentUserView(APIView):
    '''View for current logged in user profile'''
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        # display user information 
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'Unfortunately, something went wrong. Please try again later.','error:':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        # Update user detail
        try:
            #GET data and pass to serializer
            user=request.user
            serializer=UserSerializer(user,data=request.data)
            if serializer.is_valid():
                #If data is valid we can update the data
                serializer.save()
                return Response(serializer.data)
            # Tf  serializer data is invalid 
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # For unexpected errors
        except Exception as e:
            return Response({'message':'Unfortunately, something went wrong. Please try again later.','error:':str(e)},status=status.HTTP_400_BAD_REQUEST)