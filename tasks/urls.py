from django.urls import path
from . import views


app_name = 'tasks'
urlpatterns = [

    path('workspace/create/', views.WorkSpaceCreateView.as_view(), name='workspace_create'),
    path('workspace/<int:workspace_id>/', views.WorkSpaceView.as_view(), name='workspace_detail'),
    path('workspace/edit/<int:workspace_id>/', views.WorkSpaceEditView.as_view(), name='workspace_edit'),
    path('workspace/delete/<int:workspace_id>/', views.WorkSpaceDeleteView.as_view(), name='workspace_delete'),

    path('workspace/<int:workspace_id>/board/create/', views.BoardCreateView.as_view(), name='board_create'),
    path('board/<int:board_id>/', views.BoardView.as_view(), name='board_detail'),
    path('board/edit/<int:board_id>/', views.BoardEditView.as_view(), name='board_edit'),
    path('board/delete/<int:board_id>/', views.BoardDeleteView.as_view(), name='board_delete'),
    path('card/create/', views.CardCreateView.as_view(), name='create_card'),
    path('my-cards/', views.MyCardsView.as_view(), name='my_cards'),
    path('card/edit/<int:card_id>/', views.CardEditView.as_view(), name='edit_card'),
    path('card/delete/<int:card_id>/', views.CardDeleteView.as_view(), name='delete_card'),

]
