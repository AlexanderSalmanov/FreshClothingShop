from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, GuestEmail
from .forms import UserAdminChangeForm, UserAdminCreationForm
# Register your models here.

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm #update view
    add_form = UserAdminCreationForm #create view

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'admin'] # list_display attribute determines which fields will be observed instantly in the list view
    list_filter = ['admin', 'staff', 'active'] # list_filter attribute determines the list of fields via which you may filter your queryset
    # fieldsets attribute can manipulate the way the fields are displayed while viewing the user's detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'profile_pic')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(GuestEmail)
