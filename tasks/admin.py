from django.contrib import admin
from . models import BMembershipModel, WSMembershipModel, CMembershipModel,\
                     LabelModel, WorkSpaceModel, BoardModel,\
                     SubTaskModel, GMessageModel


@admin.register(WorkSpaceModel)
class WorkSpaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner','category']
    list_filter = ['category']
    search_fields = ['title']


@admin.register(BoardModel)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title','workspace','visibility','category']
    list_filter = ['category','visibility']
    search_fields = ['title']


@admin.register(LabelModel)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['title','card']
    list_filter = ['card']
    search_fields = ['card']


class SubTaskInline(admin.TabularInline):
    model = SubTaskModel


@admin.register(GMessageModel)
class GMessageAdmin(admin.ModelAdmin):
    search_fields = ['from_user', 'board']
    list_display = ['from_user', 'board', 'text'[:20]]
    list_filter = ['from_user', 'board']


