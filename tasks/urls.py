from django.urls import path
from . import views


app_name = 'tasks'
urlpatterns = [
    # workspace
    path('workspace/create/', views.WorkSpaceCreateView.as_view(), name='workspace_create'),
    path('workspace/<int:workspace_id>/', views.WorkSpaceView.as_view(), name='workspace_detail'),
    path('workspace/edit/<int:workspace_id>/', views.WorkSpaceEditView.as_view(), name='workspace_edit'),
    path('workspace/delete/<int:workspace_id>/', views.WorkSpaceDeleteView.as_view(), name='workspace_delete'),
    path('workspace/<int:workspace_id>/members/', views.WorkspaceMembersView.as_view(), name='board_members'),

    # board.py
    path('workspace/<int:workspace_id>/board.py/create/', views.BoardCreateView.as_view(), name='board_create'),
    path('board.py/<int:board_id>/', views.BoardView.as_view(), name='board_detail'),
    path('board.py/edit/<int:board_id>/', views.BoardEditView.as_view(), name='board_edit'),
    path('board.py/delete/<int:board_id>/', views.BoardDeleteView.as_view(), name='board_delete'),
    path('board.py/<int:board_id>/members/', views.BoardMembersView.as_view(), name='board_members'),

    # list
    path('board.py/<int:board_id>/list/create/', views.ListCreateView.as_view(), name='list_create'),
    path('list/edit/<int:list_id>', views.ListEditView.as_view(), name='list_edit'),
    path('list/delete/<int:list_id>', views.ListDeleteView.as_view(), name='list_delete'),

    # card
    path('card/create/<int:list_id>', views.CardCreateView.as_view(), name='card_create'),
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
    path('card/<int:sub_card_id>/sub-card/delete/', views.SubCardDeleteView.as_view(), name='sub_card_delete'),

    # workspace membership
    path('workspace/<int:workspace_id>/add-member/<int:user_id>/',
         views.AddMemberToWorkspaceView.as_view(),
         name='add_member_to_workspace'),

    path('workspace/<int:workspace_id>/remove-member/<int:user_id>/',
         views.RemoveMemberFromWorkspaceView.as_view(),
         name='remove_member_from_workspace'),

    path('workspace/<int:workspace_id>/change-member-permission/<int:user_id>/',
         views.ChangeWorkspaceMembershipPermissionView.as_view(),
         name='change_workspace_membership_permission'),

    # board.py membership
    path('board.py/<int:board_id>/add-member/<int:user_id>/',
         views.AddMemberToBoardView.as_view(),
         name='add_member_to_board'),
    path('board.py/<int:board_id>/remove-member/<int:user_id>/',
         views.RemoveMemberFromBoardView.as_view(),
         name='remove_member_from_board'),
    path('board.py/<int:board_id>/change-member-permission/<int:user_id>/',
         views.ChangeBoardMembershipPermissionView.as_view(),
         name='change_board_membership_permission'),

    # card membership
    path('card/<int:card_id>/add-member/<int:user_id>/',
         views.AddMemberToCardView.as_view(),
         name='add_member_to_board'),
    path('card/<int:card_id>/remove-member/<int:user_id>/',
         views.RemoveMemberFromCardView.as_view(),
         name='remove_member_from_board'),

]
