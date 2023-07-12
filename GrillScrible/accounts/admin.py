from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
# Register your models here.
class ProfileUserAdmin(UserAdmin):
    add_form= UserCreationForm
    form=UserChangeForm
    model=Profile
    list_display=['pk','username','email','first_name','last_name']
    add_fieldsets=UserAdmin.add_fieldsets+ (
        (None, {'fields':('email','first_name','last_name','bio','pic',)}),
    )
    fieldsets = UserAdmin.fieldsets+(
        (None, {"fields": ('bio','pic',)}),
    )
    
admin.site.register(Profile,ProfileUserAdmin)
