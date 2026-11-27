from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('role', 'bio', 'crops_grown', 'farm_size', 'location', 'phone_number', 'profile_picture')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
