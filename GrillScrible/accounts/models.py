from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from accounts.managers import ProfileUserManager
from datetime import datetime
class Profile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), unique=True,max_length=20)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(verbose_name=_("first name"), max_length=100,blank=True,null=True)
    last_name = models.CharField(verbose_name=_("last name"), max_length=100,blank=True,null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(verbose_name=_("last login"), blank=True, null=True)
    bio=models.TextField(verbose_name=_('Bio'),max_length=250,blank=True, null=True)
    pic=models.ImageField(verbose_name=_('Photo'),upload_to='profile',default='profile/default_avatar.jpg')
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = ProfileUserManager()

    def __str__(self) -> str:
        return f'{self.username} | {self.last_name}'
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
        
class Session(models.Model):
    out_token=models.ForeignKey(OutstandingToken, on_delete=models.CASCADE,null=True)
    client=models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Session for {self.client.username}"
    
    class Meta:
        verbose_name = "Session information"
        verbose_name_plural = "Sessions"
