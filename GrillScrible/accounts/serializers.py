from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import re
from django.contrib import auth
from django.contrib.auth import get_user_model
User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, style={'input_type':'password'}, write_only=True) # user can’t see that in the request sent
    password2 = serializers.CharField(max_length=68, min_length=6, style={'input_type':'password'}, write_only=True) # user can’t see that in the request sent
    class Meta:
        model = User
        fields = ['username','email', 'password', 'password2']
    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')
        pass1=attrs.get('password')
        pass2=attrs.pop('password2')
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.match(pat,email):
            raise serializers.ValidationError("Invalid Email")
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        if pass1 != pass2:
            raise serializers.ValidationError("Password and Confirm Password Does not match")
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    class Meta:
        model = User
        fields = ['password','username','tokens']
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = auth.authenticate(username=username,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'username': user.username,
            'tokens': user.tokens
        }
    
class LogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()
    
    class Meta:
        model = User
        fields= ['refresh', ]
    def save(self, **kwargs):
        try:
            RefreshToken(self.validated_data['refresh']).blacklist()
        except TokenError as e:
            raise serializers.ValidationError('bad_token') from e
            
class UserSerializer(serializers.ModelSerializer):
    authors_blogs= serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='blog_name'
    )
    class Meta:
        model=User
        exclude=['password', 'last_login', 'is_superuser','is_staff','is_active','groups','user_permissions']
        read_only_fields=['date_joined','username']
        