from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Profile
# Register your models here.
class ProfileUserAdmin(UserAdmin):
    add_form= CustomUserCreationForm
    form=CustomUserChangeForm
    model=Profile
    list_display=['pk','username','email','first_name','last_name', "is_staff", "is_active",]
    list_filter = ("username","email", "is_staff", "is_active",)
    fieldsets= (
         (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "bio", "pic")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username","email", "password1", "password2",)}),
        ("Personal Info", {"fields": ("first_name", "last_name", "bio", "pic")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    search_fields = ("username",)
    ordering = ("username",)
    
admin.site.register(Profile,ProfileUserAdmin)
