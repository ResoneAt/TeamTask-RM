from django.urls import path
from . import views


app_name = 'tasks'
urlpatterns = [
    # workspace
    path('workspace/create/', views.WorkSpaceCreateView.as_view(), name='workspace_create'),
    path('workspace/<int:workspace_id>/', views.WorkSpaceView.as_view(), name='workspace_detail'),
    path('workspace/edit/<int:workspace_id>/', views.WorkSpaceEditView.as_view(), name='workspace_edit'),
    path('workspace/delete/<int:workspace_id>/', views.WorkSpaceDeleteView.as_view(), name='workspace_delete'),

    # board
    path('workspace/<int:workspace_id>/board/create/', views.BoardCreateView.as_view(), name='board_create'),
    path('board/<int:board_id>/', views.BoardView.as_view(), name='board_detail'),
    path('board/edit/<int:board_id>/', views.BoardEditView.as_view(), name='board_edit'),
    path('board/delete/<int:board_id>/', views.BoardDeleteView.as_view(), name='board_delete'),

    # list
    path('board/<int:board_id>/list/create/', views.ListCreateView.as_view(), name='list_create'),
    path('list/edit/<int:list_id>', views.ListEditView.as_view(), name='list_edit'),
    path('list/delete/<int:list_id>', views.ListDeleteView.as_view(), name='list_delete'),

    # card
    path('card/create/', views.CardCreateView.as_view(), name='card_create'),
    path('my-cards/', views.MyCardsView.as_view(), name='my_cards'),
    path('card/edit/<int:card_id>/', views.CardEditView.as_view(), name='card_edit'),
    path('card/delete/<int:card_id>/', views.CardDeleteView.as_view(), name='card_delete'),

    # label
    path('card/<int:card_id>/label/create/', views.LabelCreateView.as_view(), name='label_create'),
    path('label/edit/<int:label_id>', views.LabelEditView.as_view(), name='label_edit'),
    path('label/delete/<int:label_id>', views.LabelDeleteView.as_view(), name='label_delete'),

    # sub card
    path('card/<int:card_id>/sub-card/create/', views.SubCardCreateView.as_view(), name='sub_card_create'),
    path('sub-card/edit/<int:sub_card_id>', views.SubCardEditView.as_view(), name='sub_card_edit'),
    path('card/<int:card_id>/sub-card/create/', views.SubCardDeleteView.as_view(), name='sub_card_delete'),

    # workspace membership
    path(),

    # board membership
    path(),

    # card membership
    path(),

]
