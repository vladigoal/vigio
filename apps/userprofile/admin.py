from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import ShopUser

class Usernline(admin.StackedInline):
    model = ShopUser
    can_delete = False
    verbose_name_plural = 'Phone'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (Usernline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)