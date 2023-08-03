from django.contrib import admin
from . models import BMembershipModel, WSMembershipModel, CMembershipModel,\
                     LabelModel, WorkSpaceModel, BoardModel,\
                     SubTaskModel, ListModel,CardModel, CardCommentModel


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
    
    
class CommentCardInline(admin.TabularInline):
    model = CardCommentModel
    fk_name = 'comment_card'
    extra = 1
    
    
@admin.register(ListModel)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'board')
    list_filter = ('title', 'board')
    search_fields = ('title',)
    ordering = ('created_at',)
 
    
@admin.register(CardModel)
class CardAdmin(admin.ModelAdmin):
    list_display = ('title', 'list','status')
    list_filter = ('title', 'status')
    search_fields = ('title','description')
    ordering = ('created_at',)
    inlines = (CommentCardInline, SubTaskInline)
    
   
@admin.register(CardCommentModel)
class CardCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'card')
    list_filter = ('user', 'card')
    search_fields = ('body',)

