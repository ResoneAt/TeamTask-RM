from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, NotificationModel , PvMessageModel
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "is_admin"]
    list_filter = ["is_admin"]

    fieldsets = [
        (None, {"fields": ["username", "email", "password"]}),
        ("Personal info", {"fields": ["full_name","image", "bio",
                                      "job_title", "work_field", ""]}),
        ("Permissions", {"fields": ["is_admin", "is_active", "is_deleted"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []
    # inlines = [UserImageInline]


@admin.register(PvMessageModel)
class PvMessageAdmin(admin.ModelAdmin):
    search_fields = ['from_user', 'to_user']
    list_display = ['from_user', 'to_user', 'text'[:20]]
    list_filter = ['from_user', 'to_user']


@admin.register(NotificationModel)
class NotificationAdmin(admin.ModelAdmin):
    search_fields = ['to_user']
    list_display = ['to_user', 'body'[:20]]
    list_filter = ['to_user']


admin.site.unregister(Group)
