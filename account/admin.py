from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from account.models import User, Otp
from . forms import UserChangeForm, UserCreationForm

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone", "email", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [   # فیلد هایی که در پنل ادمین نمایش داده میشه 
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["fullname"]}),
        ("Permissions", {"fields": ["is_admin"]}), 
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [   #زمانی که یوزر وارد میشود چه فیلد هایی نمایش بدم
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "fullname", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Otp)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
