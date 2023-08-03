from django.contrib import admin
from . models import BMembershipModel, WSMembershipModel, CMembershipModel

@admin.register(BMembershipModel)
class BMemebershipAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'board', 'permission'
    ]
    search_fields = ['board', 'user']
    list_filter = ['board']


@admin.register(WSMembershipModel)
class WSMembershipModelAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'workspace', 'permission'
    ]
    search_fields = ['workspace', 'user']
    list_filter = ['workspace']


@admin.register(CMembershipModel)
class CMembershipModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'card']
    search_fields = ['card']
    list_filter = ['card']