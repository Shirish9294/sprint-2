from django.contrib import admin
from django.utils.safestring import mark_safe

from user.models import UserProfile


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address', 'phone', 'city', 'state', 'country', 'image']


readonly_fields = ["image"]


def image(self, obj):
    return mark_safe('<img src = "{url}" />'.format(url=obj.image.url, ))


admin.site.register(UserProfile, UserProfileAdmin)
