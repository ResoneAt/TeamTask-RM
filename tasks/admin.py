from django.contrib import admin
from . models import BMembershipModel, WSMembershipModel, CMembershipModel ,LabelModel,WorkSpaceModel,BoardModel


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

