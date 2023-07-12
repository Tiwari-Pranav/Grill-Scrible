from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.
class Profile(AbstractUser):
    bio=models.CharField(verbose_name=_('Bio'),max_length=250,blank=True, null=True)
    pic=models.ImageField(verbose_name=_('Photo'),upload_to='profile',default='profile/default_avatar.jpg')
    
    def __str__(self) -> str:
        return self.username+' | '+self.last_name
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }