from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import re
from django.contrib import auth
from django.contrib.auth import get_user_model


User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    '''serializer for registration'''
    password = serializers.CharField(max_length=68, min_length=6, style={'input_type':'password'}, write_only=True) 
    # user can’t see that in the request sent
    password2 = serializers.CharField(max_length=68, min_length=6, style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username','email', 'password', 'password2']
    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')
        pass1=attrs.get('password')
        # We only need password-2 for validation
        pass2=attrs.pop('password2')
        #Email regex pattern 
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.match(pat,email):
            # Email validation
            raise serializers.ValidationError("Invalid Email")
        if not username.isalnum():
            # Username must be aphanumeric  
            raise serializers.ValidationError(self.default_error_messages)
        if pass1 != pass2:
            # Both passwords must match
            raise serializers.ValidationError("Password and Confirm Password Does not match")
        return attrs
    
    def create(self, validated_data):
        # create new user
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.ModelSerializer):
    '''Serializer for user login'''
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()
    
    def get_tokens(self, obj):
        '''Generate token'''
        #token function is defined in Profile model 
        token=obj.tokens()  
        return {
            'refresh': token['refresh'],
            'access': token['access']
        }
    class Meta:
        model = User
        fields = ['password','username','tokens']
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        # Authenticate user
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is None:
            # user is not authenticated
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            #user exist but is set inactive 
            raise AuthenticationFailed('Account disabled, contact admin')
        return user
    
class LogoutSerializer(serializers.ModelSerializer):
    '''Serializer for user logout'''
    refresh = serializers.CharField()
    class Meta:
        model = User
        fields= ['refresh', ]
        
    def validate(self, attrs):
        return attrs
            
class UserSerializer(serializers.ModelSerializer):
    '''Serializer for user profile information'''
    authors_blogs= serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='blog_name'
    )
    
    class Meta:
        model=User
        # User does not need to know
        exclude=['password', 'last_login', 'is_superuser','is_staff','is_active','groups','user_permissions']
        # Following fields cannot be updated by user
        read_only_fields=['date_joined','username']
        